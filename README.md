# Adobe Analytics Search Revenue ETL Assessment – Naveen

**Display Name:** Naveen  
**Location:** San Jose, CA  
**Date:** January 2026

## Business Problem
Analyze Adobe Analytics hit-level data to answer:  
**How much revenue comes from external search engines (Google, Yahoo, MSN/Bing) and which keywords perform best?**

**Required Output:**
- Tab-delimited file: `{YYYY-mm-dd}_SearchKeywordPerformance.tab`
  - Columns: `Search Engine Domain`, `Search Keyword`, `Revenue` (summed, sorted descending)

## Solution Overview
- **Technology**: AWS Glue (serverless Spark ETL) + PySpark
- **Single-file implementation** for easy deployment (no zip needed)
- **Key logic**:
  - Filter purchase events (`event_list` contains "1")
  - Extract search domain & keyword from referrer
  - Sum revenue from `product_list`
  - Aggregate & sort by revenue descending
- **Input**: S3 TSV/CSV file
- **Output**: Single tab-delimited file written to S3
