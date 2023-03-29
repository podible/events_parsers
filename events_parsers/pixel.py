import json
from datetime import datetime, timedelta
from locale import atoi
from urllib.parse import unquote_plus
from uuid import uuid4

import pytz

from events_parsers.helpers import check_and_reformat_ip
from events_parsers.ua_utils.user_agent import normalize_user_agent, normalize_device


def process_event(data, ip_database):
    request_timestamp = datetime.fromtimestamp(data["request_timestamp"], pytz.UTC)

    for param in data["multiValueQueryStringParameters"]:
        data[param] = data["multiValueQueryStringParameters"][param]
        try:
            data[param] = unquote_plus(data[param])
        except:
            pass
    del data["multiValueQueryStringParameters"]

    ip = None
    if "ip" in data:
        try:
            ip = check_and_reformat_ip(data["ip"])
        except ValueError:
            pass
            # Too common
            # print(f'ERROR Invalid ip in data: {data["ip"]}')  # NB: watch it in CloudWatch!

    if not ip:
        try:
            check_ip = data["multiValueHeaders"]["x-forwarded-for"][0].split(",")[0]
            try:
                ip = check_and_reformat_ip(check_ip)
            except ValueError:
                # invalid IP address, ignore it
                print(
                    f"ERROR Invalid ip ({check_ip}) in x-forwarded-for too: {data['multiValueHeaders']['x-forwarded-for']}"
                )  # NB: watch it in CloudWatch!
        except Exception as e:
            print(f"ERROR ({e}) Invalid ip in headers too: {data}")  # NB: watch it in CloudWatch!

    user_agent = "Unknown"
    try:
        if "x-device-user-agent" in data["multiValueHeaders"]:
            user_agent = data["multiValueHeaders"]["x-device-user-agent"]
        elif "ua" in data:
            user_agent = data["ua"]
        elif "user-agent" in data["multiValueHeaders"] and data["multiValueHeaders"]["user-agent"]:
            user_agent = data["multiValueHeaders"]["user-agent"]
        if isinstance(user_agent, list):
            user_agent = user_agent[0]
    except Exception as e:
        print(f"ERROR ({e}) Invalid user_agent in headers too: {data}")  # NB: watch it in CloudWatch!

    (
        advertiser,
        episode_id,
        episode_title,
        series_id,
        series_title,
        platform,
        user_id,
    ) = parse_impression_data(data)

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

    timestamp = None
    if "dt" in data:
        try:
            timestamp_seconds = atoi(data["dt"])  # since epoch UTC
            try:
                timestamp = datetime.fromtimestamp(timestamp_seconds, pytz.UTC)
            except ValueError:
                # Someone passed param dt as milliseconds instead of seconds. That's great!
                timestamp = datetime.fromtimestamp(timestamp_seconds // 1000, pytz.UTC) + timedelta(
                    milliseconds=timestamp_seconds % 1000
                )
        except:
            try:
                timestamp = datetime.strptime(data["dt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                try:
                    timestamp = datetime.strptime(data["dt"], "%Y-%m-%d %H:%M:%S UTC")
                except:
                    print(f'ERROR invalid dt in data: {data["dt"]}. Setting timestamp.')  # NB: watch it in CloudWatch!

    if timestamp is None:
        timestamp = request_timestamp

    ua_type, normalized_user_agent = normalize_user_agent(user_agent)
    trusted = ua_type != "bot"
    if trusted:
        device = normalize_device(user_agent)
    else:
        device = "Bot"

    try:
        uuid = data["uuid"]
    except KeyError:
        print(f"ERROR No UUID: {data}")  # NB: watch it in CloudWatch!
        uuid = uuid4()

    request_id = data.get("requestId") or data.get("externalCampaignId")

    return {
        "episode_id": str(episode_id) if episode_id is not None else episode_id,
        "episode_title": str(episode_title) if episode_title is not None else episode_title,
        "series_id": str(series_id) if series_id is not None else series_id,
        "series_title": str(series_title) if series_title is not None else series_title,
        "advertiser": str(advertiser) if advertiser is not None else advertiser,
        "platform": str(platform) if platform is not None else platform,
        "user_id": str(user_id) if user_id is not None else user_id,
        "user_agent": str(user_agent) if user_agent is not None else user_agent,
        "ip": str(ip) if ip is not None else ip,
        "params": json.dumps(data, default=str),
        "country": str(country) if country is not None else country,
        "city": str(city) if city is not None else city,
        "region": str(region) if region is not None else region,
        "ip_usage_type": str(ip_usage_type) if ip_usage_type is not None else ip_usage_type,
        "timestamp": timestamp,  # .strftime("%Y-%m-%d %H:%M:%S.%f"),  # for kafka
        "uuid": str(uuid) if uuid is not None else uuid,
        "trusted": trusted,
        "device": device,
        "normalized_user_agent": normalized_user_agent,
        "request_id": str(request_id) if request_id is not None else request_id,
        "clname": data.get("clname"),
        "cw_timestamp": request_timestamp,  # .strftime("%Y-%m-%d %H:%M:%S.%f"),  # for kafka
    }


def parse_impression_data(data):
    advertiser = data.get("aid") or data.get("advertiser")
    if advertiser:
        advertiser = str(advertiser).lower()

    user_id = data.get("client") or None
    platform = data.get("plt") or None
    episode_id = None
    episode_title = None
    series_id = None
    series_title = None

    # Mega universe hack for old pixels, they has been placed without proper userId
    if user_id == "betterhelp-assemble":
        user_id = "755f8993-ed38-4614-befe-0f8a8948a642"
    if user_id == "OxfordRoad":
        user_id = "574d66fb-1a31-43ec-bd16-a28cd84d396c"

    # OMNY Not lauched yet
    if platform == "omny":
        episode_id = data.get("eid") or None
        episode_title = data.get("etitle") or None
        series_title = data.get("show") or None

    # Megaphone
    if platform == "megaphone":
        episode_id = data.get("eid") or None
        series_id = data.get("pid") or None

    # Triton
    if platform == "triton":
        episode_id = data.get("eid") or None
        episode_title = data.get("etitle") or None
        primary_title = data.get("show") or None
        backup_series_title = data.get("stationname") or None
        series_title = backup_series_title if "{" in str(primary_title) else primary_title

    # Acast
    if platform == "acast":
        # Hack, because wrong advetiser lookup_name was used in the past for advertiser linqto
        if advertiser == "acast":
            advertiser = "linqto"

        try:
            eid = data.get("eid") or None
            episode_id = eid.split("/")[1]
        except:
            episode_id = None
        series_id = data.get("pid") or None

    # Adswizz
    if platform == "adswizz":
        episode_id = data.get("eid") or None
        series_id = data.get("show") or None

    # art19
    if platform == "art19":
        episode_id = data.get("eid") or None
        series_id = data.get("pid") or None

    return advertiser, episode_id, episode_title, series_id, series_title, platform, user_id
