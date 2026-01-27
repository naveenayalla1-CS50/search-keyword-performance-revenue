# transformations.py
from typing import Optional
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StringType, BooleanType

# Import your extractor functions (assumed to be in extractors.py)
from extractors import (
    extract_search_engine_domain,
    extract_search_keyword,
    extract_revenue_from_product_list,
    is_purchase_event,
)


def build_keyword_performance_df(df: DataFrame) -> DataFrame:
    """
    Transform raw Adobe Analytics hit-level data into keyword performance aggregates.

    Steps:
    1. Use UDFs to extract the domain, keyword, revenue, and buy flag.
    2. Filter to purchase events with valid search keywords.
    3. Calculate total revenue per search engine domain and phrase.
    4. Sort descending by revenue.

    Returns:
        DataFrame with columns:
            - Search Engine Domain
            - Search Keyword
            - Revenue (summed, formatted as double)
    """
    # Register UDFs with explicit return types
    udf_domain = F.udf(extract_search_engine_domain, StringType())
    udf_keyword = F.udf(extract_search_keyword, StringType())
    udf_revenue = F.udf(extract_revenue_from_product_list, DoubleType())
    udf_is_purchase = F.udf(is_purchase_event, BooleanType())

    # Enrich the DataFrame with extracted columns
    enriched_df = (
        df
        .withColumn("Search Engine Domain", udf_domain(F.col("referrer")))
        .withColumn("Search Keyword", udf_keyword(F.col("referrer")))
        .withColumn("Is Purchase", udf_is_purchase(F.col("event_list")))
        .withColumn("Revenue", udf_revenue(F.col("product_list")))
    )

    # Filter early (reduces shuffle volume)
    filtered_df = (
        enriched_df
        .filter(F.col("Is Purchase") == True)
        .filter(F.col("Search Keyword").isNotNull())
        .filter(F.col("Search Engine Domain").isNotNull())
        .filter(F.col("Revenue") > 0.0)  # optional: exclude zero-revenue purchases
    )

    # Aggregate and sort
    result_df = (
        filtered_df
        .groupBy("Search Engine Domain", "Search Keyword")
        .agg(F.sum("Revenue").alias("Revenue"))
        .orderBy(F.col("Revenue").desc())
        .select(
            F.col("Search Engine Domain"),
            F.col("Search Keyword"),
            F.format_number("Revenue", 2).alias("Revenue")  # nice formatting for output
        )
    )

    return result_df
