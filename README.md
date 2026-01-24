mindmap
  root((Adobe Analytics Search Revenue ETL – Naveen))
    Date: January 2026
    Business Problem
      External Search Engines
        Google
        Yahoo
        MSN/Bing
      Top Performing Keywords
      Revenue Attribution
        Purchase Events
        Keyword from Referrer
    Core Technology
      AWS Glue (Spark ETL)
      PySpark
      Terraform (IaC)
      S3 (Input/Output)
      CloudWatch Logs
    Data Process
      Input
        Hit-level TSV (S3)
        Key Columns
          event_list
          referrer
          product_list
      Transform
        Filter
          Purchase Event = 1
        Extract
          Search Engine Domain
          Search Keyword
        Calculate
          Revenue from product_list
        Aggregate
          Sum revenue by (Domain, Keyword)
        Sort
          Revenue DESC
      Output
        S3 Results Bucket
        Tab-separated file
        Header row included
        Naming Convention
          YYYY-mm-dd_SearchKeywordPerformance.tab
    Quality & Scale
      Correctness Checks
        Input row count > 0
        Revenue > 0 only on purchases
        Domain + keyword not null
      Unit Tests
        Referrer parsing
        Keyword extraction
        Product revenue parsing
      Scaling to 10GB+
        Spark partitioning
        Avoid coalesce early
        Write partitioned then finalize name
      Observability
        CloudWatch logs
        Glue metrics

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
  
  
