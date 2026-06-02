# extractors.py
"""
Extraction logic for search keyword performance pipeline.

This module contains pure functions for extracting structured data from
semi-structured Adobe Analytics fields. All functions use defensive
programming patterns (type checking, null handling, try-catch) to ensure
robustness against malformed input data.

Key Design Principles:
- Pure functions (no side effects) → easily testable
- Explicit return types for PySpark UDF registration
- Graceful degradation (return None/0.0 on errors)
- Type validation on all inputs
"""

from urllib.parse import urlparse, parse_qs, unquote_plus
from typing import Optional


def is_purchase_event(event_list: str) -> bool:
    """
    Determine if an Adobe event_list contains a purchase event.
    
    Adobe Analytics encodes events as comma-separated IDs. Event ID '1'
    represents a purchase/order completion event.
    
    Examples:
        - "1,2,3" → True (purchase event present)
        - "2,3,4" → False (no purchase)
        - "100,1,200" → True (1 is embedded in list)
    
    Args:
        event_list: Comma-separated Adobe event IDs (str or None)
    
    Returns:
        bool: True if event '1' is present, False otherwise
    
    Raises:
        None: Gracefully handles None and malformed input
    """
    if not event_list or not isinstance(event_list, str):
        return False
    return "1" in event_list.split(",")


def extract_search_engine_domain(referrer: str) -> Optional[str]:
    """
    Extract and validate the search engine domain from a referrer URL.
    
    This function:
    1. Parses the referrer URL
    2. Checks against a whitelist of known search engines
    3. Returns the domain only if it's a recognized search engine
    
    Supported search engines:
    - Google (google.com, www.google.com)
    - Bing (bing.com, www.bing.com)
    - Yahoo (yahoo.com, search.yahoo.com, www.yahoo.com)
    - MSN (msn.com, www.msn.com)
    
    This whitelist approach prevents poisoning the dataset with
    non-search referrers that might coincidentally contain keywords.
    
    Args:
        referrer: Full referrer URL from Adobe Analytics (str or None)
    
    Returns:
        Optional[str]: Normalized search engine domain (lowercase), or None
                      if not a recognized search engine
    
    Examples:
        >>> extract_search_engine_domain("https://www.google.com/search?q=python")
        'www.google.com'
        
        >>> extract_search_engine_domain("https://www.amazon.com/s?k=python")
        None  # Not a search engine
    """
    if not referrer or not isinstance(referrer, str):
        return None
    try:
        parsed = urlparse(referrer)
        domain = parsed.netloc.lower().strip()
        
        # Whitelist of known search engine domains
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
        # URLparse can fail on severely malformed input
        return None


def extract_search_keyword(referrer: str) -> Optional[str]:
    """
    Extract the search keyword from a referrer URL.
    
    Different search engines use different query parameter names:
    - Google/Bing/MSN: 'q' parameter
    - Yahoo: 'p' parameter
    
    The function:
    1. Validates the referrer is a known search engine
    2. Looks up the correct parameter name for that engine
    3. Extracts and URL-decodes the parameter value
    4. Returns None if any step fails (graceful degradation)
    
    This approach handles:
    - URL encoding (spaces as +, special chars as %XX)
    - Multiple query parameters
    - Missing/empty parameters
    - Malformed URLs
    
    Args:
        referrer: Full referrer URL from Adobe Analytics (str or None)
    
    Returns:
        Optional[str]: Decoded search keyword, or None if extraction fails
    
    Examples:
        >>> extract_search_keyword("https://www.google.com/search?q=python+tutorial")
        'python tutorial'
        
        >>> extract_search_keyword("https://search.yahoo.com/search?p=data+science&b=1")
        'data science'
        
        >>> extract_search_keyword("https://www.amazon.com/search?k=books")
        None  # Not a search engine
    """
    if not referrer or not isinstance(referrer, str):
        return None
    try:
        parsed = urlparse(referrer)
        domain = parsed.netloc.lower().strip()
        
        # Mapping of search engine domain to query parameter name
        param_map = {
            "google.com": "q", "www.google.com": "q",
            "bing.com": "q", "www.bing.com": "q",
            "yahoo.com": "p", "search.yahoo.com": "p", "www.yahoo.com": "p",
            "msn.com": "q", "www.msn.com": "q",
        }
        if domain not in param_map:
            return None

        # parse_qs returns dict of {param: [values]}
        params = parse_qs(parsed.query)
        param = param_map[domain]
        
        if param in params and params[param]:
            # unquote_plus handles URL decoding (+ → space, %XX → char)
            keyword = unquote_plus(params[param][0]).strip()
            return keyword if keyword else None
        return None
    except Exception:
        # URLparse or parse_qs may raise on malformed input
        return None


def extract_revenue_from_product_list(product_list: str) -> float:
    """
    Extract and sum revenue from Adobe Analytics product list.
    
    Adobe encodes product data as comma-separated list, with each product
    having semicolon-separated fields:
        product_name;category;quantity;revenue
    
    This function:
    1. Splits on commas (products)
    2. For each product, splits on semicolons
    3. Extracts the 4th field (revenue, 0-indexed as field 3)
    4. Sums all revenues
    5. Returns 0.0 for any product it can't parse (graceful degradation)
    
    Example product_list format:
        "Laptop;Electronics;1;999.99,Mouse;Accessories;2;25.00"
        
    This structure allows multiple products in a single transaction,
    enabling accurate revenue attribution per keyword.
    
    Args:
        product_list: Semicolon/comma-delimited product data (str or None)
    
    Returns:
        float: Total revenue across all products (0.0 if none can be parsed)
    
    Examples:
        >>> extract_revenue_from_product_list("Laptop;Electronics;1;999.99")
        999.99
        
        >>> extract_revenue_from_product_list(
        ...     "Laptop;Electronics;1;999.99,Mouse;Accessories;2;25.00"
        ... )
        1024.99
        
        >>> extract_revenue_from_product_list("malformed;data;here")
        0.0  # Not enough fields; gracefully returns 0.0
    """
    if not product_list or not isinstance(product_list, str):
        return 0.0
    
    total = 0.0
    try:
        for product in product_list.split(","):
            parts = product.split(";")
            # Product format: name;category;qty;revenue
            # We need at least 4 fields, revenue is at index 3
            if len(parts) >= 4:
                rev_str = parts[3].strip()
                if rev_str:
                    try:
                        total += float(rev_str)
                    except ValueError:
                        # Skip products with non-numeric revenue
                        pass
    except (ValueError, TypeError, AttributeError):
        # If splitting fails, return what we've accumulated so far
        pass
    
    return total
