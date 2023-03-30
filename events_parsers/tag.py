import json
from datetime import datetime
from urllib.parse import unquote_plus
from uuid import uuid4, UUID

import pytz

from events_parsers.helpers import check_and_reformat_ip, ZIP2DMA
from events_parsers.ua_utils.user_agent import normalize_user_agent, normalize_device


def process_event(data, ip_usage_type_db, ip_zipcode_db):
    request_timestamp = datetime.fromtimestamp(data["request_timestamp"], pytz.UTC)  # .strftime("%Y-%m-%d %H:%M:%S.%f")  # for kafka
    http_method = data["httpMethod"]
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
    elif http_method == "POST":
        try:
            data["body"] = json.loads(data["body"])
            data.update(data["body"])
            del data["body"]
        except Exception as e:
            print(f"ERROR ({e}) invalid or no body in data: {data}")  # NB: watch it in CloudWatch!
    else:
        print(f"ERROR Invalid http_method: {http_method}")  # NB: watch it in CloudWatch!

    try:
        data["headers"] = json.loads(data["headers"])
        mvh = data["headers"]
        if not mvh or not isinstance(mvh, dict):
            raise Exception("headers is not a dict")
        mvh = json.dumps(mvh, default=str)
    except Exception as e:
        print(f"ERROR ({e}) Invalid headers: {data}")  # NB: watch it in CloudWatch!
        mvh = None

    ip = None
    try:
        check_ip = data.get("ip") or data["headers"]["x-forwarded-for"][0].split(",")[0]
        try:
            ip = check_and_reformat_ip(check_ip)
        except ValueError:
            print(
                f"ERROR Invalid ip ({check_ip}) in x-forwarded-for: {data['headers']['x-forwarded-for']}"
            )  # NB: watch it in CloudWatch!
    except Exception as e:
        print(f"ERROR ({e}) Invalid ip in headers: {data}")  # NB: watch it in CloudWatch!

    user_agent, device, normalized_user_agent = None, None, None
    try:
        user_agent = data.get("useragent") or data["headers"]["user-agent"][0]
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
            postal = str(rec.postal).lower() if rec.postal != "-" else None
        except Exception as e:
            print(f"ERROR ({e}) ip_zipcode_db: {ip}", flush=True)  # NB: watch it in CloudWatch!

    dma = None
    if postal:
        try:
            dma = ZIP2DMA[postal]['name']
        except Exception as e:
            print(f"ERROR ({e}) ZIP2DMA: {postal}", flush=True)  # NB: watch it in CloudWatch!

    order_value, order_number, currency, discount_code, hashed_email, referrer, landing_url = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    action = data.get("activitykind") or data.get("action", None)
    try:
        # Handle Adjast + Paired
        if action == "event":
            if data.get("event_name") == "Trial Started":
                action = "signup"
            
            if data.get("event_name") == "Trial Converted" or data.get("event_name") == "Initial Purchase":
                action = "purchase"
    except Exception as e:
        print(f"ERROR ({e}) Invalid activitykind or action: {data}")  # NB: watch it in CloudWatch!

    params = json.dumps(
        data,
        default=str,
    )

    try:
        order_value = float(data.get("value")) if data.get("value") else None
    except Exception as e:
        print(f"ERROR ({e}) Invalid order_value: {data}")  # NB: watch it in CloudWatch!

    try:
        order_number = data.get("order_number")
        currency = data.get("currency", "USD")
        discount_code = data.get("discount_code")
        if discount_code == "null" or discount_code == "undefined" or discount_code == "":
            discount_code = None

        hashed_email = data.get("hashed_email")
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

    try:
        device_id = str(UUID(str(data["device_id"]), version=4)) if "device_id" in data else None
    except Exception as e:
        print(f"ERROR ({e}) Bad device_id in data: {data}")  # NB: watch it in CloudWatch!
        device_id = str(uuid4())

    return {
        "user_id": str(data["user_id"]) if "user_id" in data else None,
        "advertiser": advertiser,
        "ip": ip,
        "user_agent": user_agent,
        "device": device,
        "normalized_user_agent": normalized_user_agent,
        "params": params,
        "headers": mvh,
        "action": action,
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
        "hashed_email": hashed_email,
        "referrer": referrer,
        "landing_url": landing_url,
        "DMA": dma
    }
