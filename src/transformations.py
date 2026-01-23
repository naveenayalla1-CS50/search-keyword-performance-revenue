from pyspark.sql import DataFrame, functions as F
from pyspark.sql.types import DoubleType, StringType, BooleanType

from extractors import (
    extract_search_engine_domain,
    extract_search_keyword,
    extract_revenue_from_product_list,
    is_purchase_event,
)


def build_keyword_performance_df(df: DataFrame) -> DataFrame:
    udf_domain = F.udf(extract_search_engine_domain, StringType())
    udf_keyword = F.udf(extract_search_keyword, StringType())
    udf_revenue = F.udf(extract_revenue_from_product_list, DoubleType())
    udf_purchase = F.udf(is_purchase_event, BooleanType())

    enriched_df = (
        df
        .withColumn("Search Engine Domain", udf_domain(F.col("referrer")))
        .withColumn("Search Keyword", udf_keyword(F.col("referrer")))
        .withColumn("Is Purchase", udf_purchase(F.col("event_list")))
        .withColumn("Revenue", udf_revenue(F.col("product_list")))
    )

    return (
        enriched_df
        .filter(F.col("Is Purchase") == True)
        .filter(F.col("Search Keyword").isNotNull())
        .groupBy("Search Engine Domain", "Search Keyword")
        .agg(F.sum("Revenue").alias("Revenue"))
        .orderBy(F.col("Revenue").desc())
    )
