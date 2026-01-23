from extractors import (
    extract_search_engine_domain,
    extract_search_keyword,
    extract_revenue_from_product_list,
    is_purchase_event,
)

def test_domain():
    assert extract_search_engine_domain(
        "http://search.yahoo.com/search?p=test"
    ) == "search.yahoo.com"


def test_keyword_google():
    assert extract_search_keyword(
        "https://www.google.com/search?q=Laffy+Taffy"
    ) == "Laffy Taffy"


def test_keyword_yahoo():
    assert extract_search_keyword(
        "http://search.yahoo.com/search?p=marketing"
    ) == "marketing"


def test_purchase_event():
    assert is_purchase_event("2,10,1") is True
    assert is_purchase_event("2,10") is False


def test_product_revenue():
    product_list = "Candy;Laffy Taffy;1;12.95"
    assert extract_revenue_from_product_list(product_list) == 12.95
