import json
from datetime import datetime
from uuid import uuid4

import pytz

from events_parsers.helpers import check_and_reformat_ip
from events_parsers.ua_utils.user_agent import normalize_user_agent, normalize_device


def process_event(data, ip_database):
    if data["httpMethod"] != "GET":
        return

    mvh = data["multiValueHeaders"]
    if any(
        [
            zero_bytes_check in json.dumps(mvh, default=str).lower()
            for zero_bytes_check in ['"range": ["bytes=0-1"]', '"range": ["bytes=0-0"]']
        ]
    ):
        return

    user_agent = "Unknown"
    try:
        user_agent = mvh["user-agent"][0]
    except:
        pass
        # Too common
        # print(f"ERROR ({e}) Invalid UA in headers: {data}")  # NB: watch it in CloudWatch!

    ip = None
    try:
        check_ip = mvh["x-forwarded-for"][0].split(",")[0]
        try:
            ip = check_and_reformat_ip(check_ip)
        except ValueError:
            print(f"ERROR Invalid ip: {check_ip}")  # NB: watch it in CloudWatch!
    except Exception as e:
        print(f"ERROR ({e}) No ip: {data}")  # NB: watch it in CloudWatch!

    country, city, region, ip_usage_type = None, None, None, None
    if ip:
        try:
            rec = ip_database.get_all(ip)
            country = rec.country_short.lower() if rec.country_short != "-" else None
            city = rec.city if rec.city != "-" else None
            region = rec.region if rec.region != "-" else None
            ip_usage_type = rec.usage_type if rec.usage_type != "-" else None
        except Exception as e:
            print(f"ERROR ({e}) i2l_database: {ip}")  # NB: watch it in CloudWatch!

    try:
        redirect_url = data["redirectTarget"]
    except KeyError:
        print(f"ERROR No redirect_url: {data}")  # NB: watch it in CloudWatch!
        redirect_url = None

    try:
        uuid = data["uuid"]
    except KeyError:
        print(f"ERROR No UUID: {data}")  # NB: watch it in CloudWatch!
        uuid = uuid4()

    try:
        incoming_path = data["incomingPath"]
    except KeyError:
        print(f"ERROR No incomingPath: {data}")  # NB: watch it in CloudWatch!
        incoming_path = None

    ua_type, normalized_user_agent = normalize_user_agent(user_agent)
    trusted = ua_type not in ["bot", "library"]
    if ua_type != "bot":
        device = normalize_device(user_agent)
    else:
        device = "Bot"

    request_timestamp = datetime.fromtimestamp(data["request_timestamp"], pytz.UTC)  # .strftime("%Y-%m-%d %H:%M:%S.%f")  # for kafka

    return {
        "ip": str(ip) if ip is not None else ip,
        "user_agent": str(user_agent) if user_agent is not None else user_agent,
        "redirect_url": str(redirect_url) if redirect_url is not None else redirect_url,
        "incoming_path": str(incoming_path) if incoming_path is not None else incoming_path,
        "headers": json.dumps(mvh, default=str),
        "timestamp": request_timestamp,
        "country": str(country) if country is not None else country,
        "city": str(city) if city is not None else city,
        "region": str(region) if region is not None else region,
        "ip_usage_type": str(ip_usage_type) if ip_usage_type is not None else ip_usage_type,
        "uuid": str(uuid) if uuid is not None else uuid,
        "trusted": trusted,
        "device": device,
        "normalized_user_agent": normalized_user_agent,
    }