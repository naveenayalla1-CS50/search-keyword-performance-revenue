# Adobe Analytics Search Revenue ETL Assessment – Naveen

**Display Name:** Naveen  
**Location:** San Jose, CA  
**Date:** January 2026

## Business Problem
The client wants to understand:  
**How much revenue is generated from external search engines (Google, Yahoo, MSN/Bing) and which keywords perform best based on revenue?**

This solution processes Adobe Analytics hit-level data (tab-separated file), filters purchase events, extracts search domain & keyword from referrer, aggregates revenue from product_list, and provides sorted output + insights.

**Added Value:**
- Monthly revenue trends per keyword (to spot seasonality)
- Bar chart visualization of top 10 keywords by revenue
- Scalable to 10 GB+ uncompressed files using AWS Glue (serverless Spark ETL)

## Solution Architecture
- **Core Technology:** AWS Glue + PySpark
- **Deployment:** Terraform (IaC) for repeatable provisioning of IAM role + Glue job
- **Quality:** Unit tests for referrer parsing and revenue calculation
- **Output Files** (written to S3):
  - `{YYYY-mm-dd}_SearchKeywordPerformance.tab` → total revenue, sorted descending
  - `{YYYY-mm-dd}_MonthlySearchTrends.tab` → monthly breakdown
  - `{YYYY-mm-dd}_Top10_Keyword_Revenue_Chart.png` → top 10 keywords visualization

## Repository Contents
