import re
from .devices import devices
from .browsers import browsers
from .apps import apps
from .bots import bots
from .libraries import libraries


# Source of regex patterns: https://github.com/opawg/user-agents-v2

UA_TYPES = (
    ("bot", bots),
    ("app", apps),
    ("library", libraries),
    ("browser", browsers),
)


def normalize_user_agent(user_agent: str) -> tuple[str, str]:
    if not user_agent:
        return "other", "Other"

    for ua_db in UA_TYPES:
        ua_type = ua_db[0]
        db = ua_db[1]
        for entity in db:
            if re.search(entity["pattern"], user_agent):
                return ua_type, entity["name"]

    return "other", "Other"


def normalize_device(ua: str) -> str:
    if not ua:
        return "Other"

    for item in devices:
        if re.search(item["pattern"], ua):
            return item["name"]

    return "Other"
