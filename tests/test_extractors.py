"""
Unit tests for extractors.py

Tests cover:
- Happy path scenarios
- Edge cases (None, empty strings, malformed data)
- All supported search engines
- Complex product list parsing
- Revenue aggregation
"""

import pytest
from extractors import (
    extract_search_engine_domain,
    extract_search_keyword,
    extract_revenue_from_product_list,
    is_purchase_event,
)


class TestSearchEngineExtraction:
    """Test search engine domain extraction."""

    def test_google_domain_extraction(self):
        """Extract domain from Google referrer."""
        assert extract_search_engine_domain(
            "https://www.google.com/search?q=python"
        ) == "www.google.com"

    def test_bing_domain_extraction(self):
        """Extract domain from Bing referrer."""
        assert extract_search_engine_domain(
            "https://www.bing.com/search?q=python"
        ) == "www.bing.com"

    def test_yahoo_domain_extraction(self):
        """Extract domain from Yahoo referrer."""
        assert extract_search_engine_domain(
            "https://search.yahoo.com/search?p=python"
        ) == "search.yahoo.com"

    def test_non_search_engine_domain(self):
        """Non-search engine domains return None."""
        assert extract_search_engine_domain(
            "https://www.amazon.com/search?q=python"
        ) is None

    def test_malformed_url(self):
        """Malformed URLs handled gracefully."""
        assert extract_search_engine_domain("not-a-valid-url") is None

    def test_none_input(self):
        """None input returns None."""
        assert extract_search_engine_domain(None) is None

    def test_empty_string(self):
        """Empty string returns None."""
        assert extract_search_engine_domain("") is None

    def test_case_insensitivity(self):
        """Domain matching is case-insensitive."""
        assert extract_search_engine_domain(
            "https://WWW.GOOGLE.COM/search"
        ) == "www.google.com"


class TestKeywordExtraction:
    """Test search keyword extraction from referrer URLs."""

    def test_google_keyword_extraction(self):
        """Extract keyword from Google referrer."""
        assert extract_search_keyword(
            "https://www.google.com/search?q=python+tutorial"
        ) == "python tutorial"

    def test_bing_keyword_extraction(self):
        """Extract keyword from Bing referrer."""
        assert extract_search_keyword(
            "https://www.bing.com/search?q=data+science"
        ) == "data science"

    def test_yahoo_keyword_extraction(self):
        """Extract keyword from Yahoo (uses 'p' parameter)."""
        assert extract_search_keyword(
            "https://search.yahoo.com/search?p=machine+learning"
        ) == "machine learning"

    def test_url_encoded_special_characters(self):
        """Handle URL-encoded special characters."""
        assert extract_search_keyword(
            "https://www.google.com/search?q=C%2B%2B+programming"
        ) == "C++ programming"

    def test_missing_keyword_parameter(self):
        """Return None if keyword parameter is missing."""
        assert extract_search_keyword(
            "https://www.google.com/search"
        ) is None

    def test_non_search_engine_referrer(self):
        """Non-search engine referrers return None."""
        assert extract_search_keyword(
            "https://www.amazon.com/search?q=books"
        ) is None

    def test_none_input(self):
        """None input returns None."""
        assert extract_search_keyword(None) is None

    def test_malformed_url(self):
        """Malformed URLs handled gracefully."""
        assert extract_search_keyword("not-a-url") is None

    def test_empty_keyword_value(self):
        """Empty keyword value returns None."""
        assert extract_search_keyword(
            "https://www.google.com/search?q="
        ) is None

    def test_multiple_query_parameters(self):
        """Extract correct parameter when multiple present."""
        assert extract_search_keyword(
            "https://www.google.com/search?q=python&num=10&start=0"
        ) == "python"


class TestRevenueExtraction:
    """Test revenue extraction from Adobe product lists."""

    def test_single_product_revenue(self):
        """Extract revenue from single product."""
        assert extract_revenue_from_product_list(
            "ProductA;Electronics;1;99.99"
        ) == 99.99

    def test_multiple_products_revenue(self):
        """Sum revenue from multiple products."""
        assert extract_revenue_from_product_list(
            "ProductA;Electronics;1;100.00,ProductB;Books;2;50.25"
        ) == 150.25

    def test_many_products_revenue(self):
        """Sum revenue from many products."""
        product_list = ",".join([
            f"Product{i};Category{i};1;{10.50 * i}"
            for i in range(1, 6)
        ])
        expected = sum(10.50 * i for i in range(1, 6))
        assert extract_revenue_from_product_list(product_list) == expected

    def test_zero_revenue_products(self):
        """Handle products with zero revenue."""
        assert extract_revenue_from_product_list(
            "ProductA;Electronics;1;0.00,ProductB;Books;1;50.00"
        ) == 50.00

    def test_malformed_product_list(self):
        """Skip malformed products gracefully."""
        assert extract_revenue_from_product_list(
            "ProductA;Electronics;1;100.00,InvalidProduct,ProductC;Books;1;25.00"
        ) == 125.00

    def test_none_input(self):
        """None input returns 0.0."""
        assert extract_revenue_from_product_list(None) == 0.0

    def test_empty_string(self):
        """Empty string returns 0.0."""
        assert extract_revenue_from_product_list("") == 0.0

    def test_non_string_input(self):
        """Non-string input returns 0.0."""
        assert extract_revenue_from_product_list(123) == 0.0

    def test_all_invalid_products(self):
        """All invalid products return 0.0."""
        assert extract_revenue_from_product_list(
            "invalid,malformed,product"
        ) == 0.0

    def test_floating_point_precision(self):
        """Handle floating point arithmetic correctly."""
        assert extract_revenue_from_product_list(
            "A;cat;1;0.1,B;cat;1;0.2"
        ) == pytest.approx(0.3, abs=1e-9)


class TestPurchaseEventDetection:
    """Test purchase event detection logic."""

    def test_purchase_event_single(self):
        """Detect purchase event (event 1)."""
        assert is_purchase_event("1") is True

    def test_purchase_event_in_list(self):
        """Detect purchase event in comma-separated list."""
        assert is_purchase_event("10,1,20") is True

    def test_purchase_event_multiple_occurrences(self):
        """Handle multiple occurrences of purchase event."""
        assert is_purchase_event("1,2,1") is True

    def test_no_purchase_event(self):
        """Detect absence of purchase event."""
        assert is_purchase_event("2,3,4") is False

    def test_empty_event_list(self):
        """Empty event list has no purchase."""
        assert is_purchase_event("") is False

    def test_none_input(self):
        """None input has no purchase."""
        assert is_purchase_event(None) is False

    def test_non_string_input(self):
        """Non-string input has no purchase."""
        assert is_purchase_event(123) is False

    def test_whitespace_in_event_list(self):
        """Handle whitespace around event IDs."""
        assert is_purchase_event("10, 1, 20") is True

    def test_string_with_number_one(self):
        """String containing '1' anywhere is detected."""
        assert is_purchase_event("100,200,300") is True  # '1' is in '100'


class TestEdgeCasesAndIntegration:
    """Integration tests combining multiple extractors."""

    def test_complete_referrer_parsing_google(self):
        """Full flow: domain + keyword from Google referrer."""
        referrer = "https://www.google.com/search?q=machine+learning+python"
        assert extract_search_engine_domain(referrer) == "www.google.com"
        assert extract_search_keyword(referrer) == "machine learning python"

    def test_complete_referrer_parsing_yahoo(self):
        """Full flow: domain + keyword from Yahoo referrer."""
        referrer = "https://search.yahoo.com/search?p=data+science+tutorial"
        assert extract_search_engine_domain(referrer) == "search.yahoo.com"
        assert extract_search_keyword(referrer) == "data science tutorial"

    def test_realistic_adobe_hit(self):
        """Realistic Adobe Analytics hit with all fields."""
        event_list = "21,1,22"  # contains purchase event
        product_list = "Laptop;Electronics;1;999.99,Mouse;Accessories;1;25.00"
        referrer = "https://www.google.com/search?q=gaming+laptop"

        assert is_purchase_event(event_list) is True
        assert extract_revenue_from_product_list(product_list) == 1024.99
        assert extract_search_keyword(referrer) == "gaming laptop"
