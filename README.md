# Adobe Analytics Search Revenue ETL Assessment – Naveen

**Date:** January 2026

mindmap
  root((Search Revenue ETL))
    Business Goal
      Revenue Analysis
      Keyword Performance
      Search Engines
    Technology Stack
      AWS Glue
      PySpark
      Terraform
    Data Pipeline
      Input: Adobe Analytics Data
      Process: Filter & Aggregate
      Output: S3 Storage
    Output File Details
      Tab-separated format
      Sorted by Revenue
      Naming: YYYY-mm-dd_SearchKeywordPerformance.tab

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
  
  
