import re
from typing import Optional, List

from tld import get_tld, Result
from tld.exceptions import TldBadUrl, TldDomainNotFound


def get_normalized_referrer(
        referrer: Optional[str],
        landing_url: Optional[str],
        advertiser: Optional[str]
) -> Optional[str]:
    try:
        urls = parse_urls([referrer, landing_url])

        parsed_referrer = urls[0]
        urls = list(filter(None, urls))

        if not urls:
            return None

        if has_google_utm_in_query(list(map(lambda url: url.parsed_url.query, urls))):
            return 'google ads'

        if not advertiser or parsed_referrer.domain.find(advertiser) == -1:
            return parsed_referrer.domain

    except:
        pass

    return None


def parse_urls(urls: List[str]) -> List[Optional[Result]]:
    result = []
    for url in urls:
        if not url or url == '_':
            result.append(None)
            continue

        try:
            parsed = get_tld(url, as_object=True)
            if parsed.parsed_url.scheme in ('http', 'https'):
                result.append(parsed)
            else:
                result.append(None)

        except (TldDomainNotFound, TldBadUrl):
            result.append(None)

    return result


def has_google_utm_in_query(queries: List[str]) -> bool:
    for query in queries:
        if re.match(r'.*utm_source=google.*', query):
            return True

    return False
