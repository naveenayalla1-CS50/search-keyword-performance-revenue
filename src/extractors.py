from urllib.parse import urlparse, parse_qs, unquote

SEARCH_PARAMS = ["q", "p"]  # Google/Bing, Yahoo


def extract_search_engine_domain(referrer: str) -> str | None:
    if not referrer:
        return None
    try:
        return urlparse(referrer).netloc.replace("www.", "")
    except Exception:
        return None


def extract_search_keyword(referrer: str) -> str | None:
    if not referrer:
        return None
    try:
        query = parse_qs(urlparse(referrer).query)
        for param in SEARCH_PARAMS:
            if param in query:
                value = query[param][0]
                return unquote(value.replace("+", " "))
        return None
    except Exception:
        return None


def is_purchase_event(event_list: str) -> bool:
    if not event_list:
        return False
    return "1" in event_list.split(",")


def extract_revenue_from_product_list(product_list: str) -> float:
    if not product_list:
        return 0.0

    revenue = 0.0
    products = product_list.split(",")

    for product in products:
        parts = product.split(";")
        if len(parts) >= 4:
            try:
                revenue += float(parts[3])
            except ValueError:
                continue
    return revenue
