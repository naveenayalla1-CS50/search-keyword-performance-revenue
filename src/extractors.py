# extractors.py
from urllib.parse import urlparse, parse_qs, unquote_plus
from typing import Optional


def is_purchase_event(event_list: str) -> bool:
    """Check if '1' (purchase) is present in event_list."""
    if not event_list or not isinstance(event_list, str):
        return False
    return "1" in event_list.split(",")


def extract_search_engine_domain(referrer: str) -> Optional[str]:
    """Extract domain only if it's a known search engine."""
    if not referrer or not isinstance(referrer, str):
        return None
    try:
        parsed = urlparse(referrer)
        domain = parsed.netloc.lower().strip()
        known_search_domains = {
            "google.com", "www.google.com",
            "bing.com", "www.bing.com",
            "yahoo.com", "search.yahoo.com", "www.yahoo.com",
            "msn.com", "www.msn.com",
        }
        if domain in known_search_domains:
            return domain
        return None
    except Exception:
        return None


def extract_search_keyword(referrer: str) -> Optional[str]:
    """Extract keyword from referrer query param of known search engines."""
    if not referrer or not isinstance(referrer, str):
        return None
    try:
        parsed = urlparse(referrer)
        domain = parsed.netloc.lower().strip()
        param_map = {
            "google.com": "q", "www.google.com": "q",
            "bing.com": "q", "www.bing.com": "q",
            "yahoo.com": "p", "search.yahoo.com": "p", "www.yahoo.com": "p",
            "msn.com": "q", "www.msn.com": "q",
        }
        if domain not in param_map:
            return None

        params = parse_qs(parsed.query)
        param = param_map[domain]
        if param in params and params[param]:
            keyword = unquote_plus(params[param][0]).strip()
            return keyword if keyword else None
        return None
    except Exception:
        return None


def extract_revenue_from_product_list(product_list: str) -> float:
    """Sum revenue from all products (4th field after ;)."""
    if not product_list or not isinstance(product_list, str):
        return 0.0
    total = 0.0
    try:
        for product in product_list.split(","):
            parts = product.split(";")
            if len(parts) >= 4:
                rev_str = parts[3].strip()
                if rev_str:
                    total += float(rev_str)
    except (ValueError, TypeError):
        pass  # skip malformed products
    return total
