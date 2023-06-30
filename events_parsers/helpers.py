import ipaddress
import re
from typing import Optional

from tld import get_tld
from tld.exceptions import TldBadUrl, TldDomainNotFound


def check_and_reformat_ip(ip):
    ipaddress.ip_address(ip)
    if ":" in ip:
        ip = ":".join(ip.split(":")[:4])
        if not ip.endswith(":"):
            return ip + "::"
        else:
            return ip + ":"
    return ip


def get_normalized_referrer(referrer: Optional[str]) -> Optional[str]:
    if referrer and referrer != '_':
        try:
            parsed_referrer = get_tld(referrer, as_object=True)
            if parsed_referrer.parsed_url.scheme not in ('http', 'https'):
                return None

            if re.match('.*utm_source=google.*', parsed_referrer.parsed_url.query):
                return 'Google ads'

            return parsed_referrer.domain.capitalize()

        except (TldDomainNotFound, TldBadUrl):
            pass

    return None
