import json
import hashlib
import re
from datetime import datetime
from urllib.parse import unquote_plus
from uuid import uuid4

import pytz

from events_parsers.helpers import check_and_reformat_ip
from events_parsers.dma import ZIP2DMA
from events_parsers.ua_utils.user_agent import normalize_user_agent, normalize_device

EVENT_MAPPING = {
    "Trial Started": "signup",  # Adjast
    "Trial Converted": "purchase",  # Adjast
    "Initial Purchase": "purchase",  # Paired
    "SEGMENT_M_SUBSCRIPTION_PAGE_PURCHASE_SUCCESS": "signup",  # DoorDash
    "SEGMENT_M_FIRST_ORDER_COMPLETE": "lead",  # DoorDash
    "SEGMENT_ALL-ORDER_SUCCESS": "purchase",  # DoorDash
}


def process_event(data, ip_usage_type_db, ip_zipcode_db):
    request_timestamp = datetime.fromtimestamp(data["request_timestamp"], pytz.UTC)  # .strftime("%Y-%m-%d %H:%M:%S.%f")  # for kafka
    http_method = data["httpMethod"]

    headers = None
    if http_method == "GET":
        try:
            data["params"] = json.loads(data["params"])
            for param in data["params"]:
                data[param] = data["params"][param]
                if isinstance(data[param], list):
                    unquoted = []
                    for val in data[param]:
                        try:
                            unquoted.append(unquote_plus(val))
                        except:
                            unquoted.append(val)
                    data[param] = unquoted
                    if param != "h":
                        data[param] = data[param][0]
            del data["params"]
        except Exception as e:
            print(f"ERROR ({e}) invalid or no params in data: {data}")  # NB: watch it in CloudWatch!
        try:
            headers = data.pop("headers")
            headers = json.loads(headers)
        except Exception as e:
            print(f"ERROR ({e}) invalid or no headers in data: {data}")  # NB: watch it in CloudWatch!
    elif http_method == "POST":
        try:
            data["body"] = json.loads(data["body"])
            data.update(data["body"])
            del data["body"]
        except Exception as e:
            print(f"ERROR ({e}) invalid or no body in data: {data}")  # NB: watch it in CloudWatch!
    else:
        print(f"ERROR Invalid http_method: {http_method}")  # NB: watch it in CloudWatch!

    ip = None
    try:
        check_ip = data.get("ip") or headers["x-forwarded-for"][0].split(",")[0]
        try:
            ip = check_and_reformat_ip(check_ip)
        except ValueError:
            print(
                f"ERROR Invalid ip ({check_ip}) in x-forwarded-for: {headers['x-forwarded-for']}"
            )  # NB: watch it in CloudWatch!
    except Exception as e:
        print(f"ERROR ({e}) Invalid ip in headers: {headers}")  # NB: watch it in CloudWatch!

    user_agent, device, normalized_user_agent = None, None, None
    try:
        user_agent = data.get("useragent") or headers["user-agent"][0]
        ua_type, normalized_user_agent = normalize_user_agent(user_agent)
        if ua_type != "bot":
            device = normalize_device(user_agent)
        else:
            device = "Bot"
    except Exception as e:
        print(f"ERROR ({e}) Failed to get User Agent, proceeding: {data}")

    country, city, region, ip_usage_type, postal = None, None, None, None, None
    if ip:
        try:
            rec = ip_usage_type_db.get_all(ip)
            country = str(rec.country_short).lower() if rec.country_short != "-" else None
            city = str(rec.city) if rec.city != "-" else None
            region = str(rec.region) if rec.region != "-" else None
            ip_usage_type = str(rec.usage_type) if rec.usage_type != "-" else None
        except Exception as e:
            print(f"ERROR ({e}) ip_usage_type_db: {ip}", flush=True)  # NB: watch it in CloudWatch!

        try:
            rec = ip_zipcode_db.get_all(ip)
            postal = str(rec.zipcode).lower() if rec.zipcode != "-" else None
        except Exception as e:
            print(f"ERROR ({e}) ip_zipcode_db: {ip}", flush=True)  # NB: watch it in CloudWatch!

    dma = None
    if postal and country == 'us':
        try:
            dma = ZIP2DMA[postal]['name']
        except Exception as e:
            print(f"ERROR ({e}) ZIP2DMA: {postal}", flush=True)  # NB: watch it in CloudWatch!

    order_value, order_number, currency, discount_code, referrer, landing_url = (
        None,
        None,
        None,
        None,
        None,
        None,
    )

    action = None
    raw_action = None
    try:
        activity_kind = data.get("activitykind")
        if activity_kind == "event":
            event_name = data.get("event_name")
            action = EVENT_MAPPING.get(event_name) or event_name
            raw_action = event_name
        elif activity_kind:
            action = activity_kind
            raw_action = activity_kind
        else:
            action = data.get("action")
            raw_action = data.get("action")

    except Exception as e:
        print(f"ERROR ({e}) Invalid action in data: {data}")  # NB: watch it in CloudWatch!

    try:
        order_value = float(data.get("value")) if data.get("value") else None
    except Exception as e:
        print(f"ERROR ({e}) Invalid order_value: {data}")  # NB: watch it in CloudWatch!

    try:
        order_number = data.get("order_number")
        if order_number == "null" or order_number == "undefined" or order_number == "":
            order_number = None

        currency = data.get("currency", "USD")
        discount_code = data.get("discount_code")
        if discount_code == "null" or discount_code == "undefined" or discount_code == "":
            discount_code = None

        referrer = unquote_plus(str(data["referrer"])) if "referrer" in data else None
        landing_url = unquote_plus(str(data["url"])) if "url" in data else None
    except Exception as e:
        print(f"ERROR ({e}) Invalid params: {data}")  # NB: watch it in CloudWatch!

    try:
        uuid = str(data["uuid"])
    except Exception as e:
        print(f"ERROR ({e}) Bad UUID in data: {data}")  # NB: watch it in CloudWatch!
        uuid = str(uuid4())

    advertiser = str(data["advertiser"].lower()) if "advertiser" in data else None
    if advertiser == "bookshop.org":
        advertiser = "bookshoporg"

    if advertiser == "acastself-serve":
        advertiser = "acastselfserve"

    try:
        device_id = str(data["device_id"]) if "device_id" in data else None
    except Exception as e:
        print(f"ERROR ({e}) Bad device_id in data: {data}")  # NB: watch it in CloudWatch!
        device_id = str(uuid4())

    email_md5, email_sha256 = None, None
    try:
        if 'hashed_email' in data:
            email_raw = data.pop('hashed_email')
            if email_raw:
                email_raw = str(email_raw).lower().strip()
                if '@' in email_raw:
                    email_md5 = hashlib.md5(email_raw.encode('utf-8')).hexdigest().lower()
                    email_sha256 = hashlib.sha256(email_raw.encode('utf-8')).hexdigest().lower()
                elif len(email_raw) == 32:
                    email_md5 = email_raw
                elif len(email_raw) == 64:
                    email_sha256 = email_raw
                else:
                    print(f"ERROR Bad hashed_email: {email_raw}")  # NB: watch it in CloudWatch!
    except Exception as e:
        print(f"ERROR ({e}) Bad hashed_email in data: {data}")  # NB: watch it in CloudWatch!


    idfa, gaid = None, None
    try:
        idfa = data.get('idfa').lower() if 'idfa' in data else None
    except Exception as e:
        print(f"ERROR ({e}) Bad idfa in data: {data}")

    try:
        # Google Advertising ID (GAID) For Singular integration
        # Unhashed Android ID - this identifier is available if the advertising identifier (AIFA) is not available on the device. As this identifier is not always available, we recommend using {AIFA}, or {COALESCE|{AIFA},{ANDI}} to ensure a value is always passed.
        aifa = data.get('aifa').lower() if 'aifa' in data else None
        andi = data.get('andi').lower() if 'andi' in data else None
        gaid = data.get('gaid').lower() if 'gaid' in data else None

        gaid = gaid or aifa or andi
    except Exception as e:
        print(f"ERROR ({e}) Bad gaid in data: {data}")

    try:
        if 'x-forwarded-url' in headers:
            headers['x-forwarded-url'] = re.sub(
                r'hashed_email=[^&]*&?', '',
                headers['x-forwarded-url'][0]
            )
    except Exception as e:
        print(f"ERROR ({e}) clearing out hashed_email from x-forwarded-url in data: {data}")  # NB: watch it in CloudWatch!

    try:
        headers = json.dumps(headers, default=str)
    except Exception as e:
        try:
            # in case if in headers is smth not serializable
            if headers is not None:
                headers = str(headers)
        except:
            headers = None
        print(f"ERROR ({e}) Invalid headers: {headers}")  # NB: watch it in CloudWatch!

    params = json.dumps(
        data,
        default=str,
    )

    return {
        "user_id": str(data["user_id"]) if "user_id" in data else None,
        "advertiser": advertiser,
        "ip": ip,
        "user_agent": user_agent,
        "device": device,
        "normalized_user_agent": normalized_user_agent,
        "params": params,
        "headers": headers,
        "action": action,
        "raw_action": raw_action,
        "country": country,
        "city": city,
        "region": region,
        "ip_usage_type": ip_usage_type,
        "postal": postal,
        "timestamp": request_timestamp,
        "uuid": uuid,
        "device_id": device_id,
        "order_value": order_value,
        "order_number": order_number,
        "currency": currency,
        "discount_code": discount_code,
        "referrer": referrer,
        "landing_url": landing_url,
        "DMA": dma,
        "email_md5": email_md5,
        "email_sha256": email_sha256,
        "idfa": idfa,
        "gaid": gaid,
    }
