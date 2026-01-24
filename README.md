mindmap
  root((Adobe Analytics Search Revenue ETL))
    Business Problem
      External Search Engines
        Google
        Yahoo
        MSN/Bing
      Top Performing Keywords
      Monthly Revenue Trends
    Core Technology
      AWS Glue
      PySpark
      Terraform IaC
    Data Process
      Input: Hit-level Data
      Filter: Purchase Events
      Extract: Referrer & Keywords
      Aggregate: Product List Revenue
    Output File (S3)
      Tab-separated format
      Sorted Descending
      Naming: YYYY-mm-dd_SearchKeywordPerformance.tab
    Quality & Scale
      Unit Tests
      Scalable to 10GB+


# Adobe Analytics Search Revenue ETL Assessment – Naveen

**Date:** January 2026

## Business Problem
The client wants to understand:  
**How much revenue is generated from external search engines (Google, Yahoo, MSN/Bing) and which keywords perform best based on revenue?**

This solution processes Adobe Analytics hit-level data (tab-separated file), filters purchase events, extracts search domain & keyword from referrer, aggregates revenue from product_list, and provides sorted output + insights.

**Added Value:**
- Monthly revenue trends per keyword (to spot seasonality)
- Scalable to 10 GB+ uncompressed files using AWS Glue (serverless Spark ETL)

## Solution Architecture
- **Core Technology:** AWS Glue + PySpark
- **Deployment:** Terraform (IaC) for repeatable provisioning of IAM role + Glue job
- **Quality:** Unit tests for referrer parsing and revenue calculation
- **Output Files** (written to S3):
  - `{YYYY-mm-dd}_SearchKeywordPerformance.tab` → total revenue, sorted descending
  
  
