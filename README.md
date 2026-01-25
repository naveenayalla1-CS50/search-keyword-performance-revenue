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


##  Solution Overview

**Key features:**

- Reads hit-level TSV data from Amazon S3
- Filters purchase events (`event_list` contains `1`)
- Extracts:
  - External search engine domain (Google, Yahoo, MSN/Bing)
  - Search keyword from referrer query parameters
- Aggregates revenue from the `product_list` field
- Writes a tab-delimited, sorted output file to S3

---

##  Technology Stack

- **Apache Spark (PySpark)**
- **AWS Glue (Spark ETL)**
- **Amazon S3** (input & output storage)
- **CloudWatch Logs & Metrics**
- **Terraform (IaC)** – optional, for provisioning Glue jobs and IAM roles

---

##  Data Processing Logic

### Input
- **Source:** Adobe Analytics hit-level data (TSV)
- **Location:** Amazon S3
- **Key columns used:**
  - `event_list`
  - `referrer`
  - `product_list`

### Transformations
1. Filter rows where `event_list` contains purchase event (`1`)
2. Extract external search engine domain from `referrer`
3. Extract search keyword from referrer query parameters
4. Parse revenue from `product_list` (4th semicolon-delimited field)
5. Aggregate total revenue by `(Search Engine Domain, Search Keyword)`
6. Sort results by revenue (descending)

### Output
- **Format:** Tab-separated (`.tab`)
- **Header:** Included
- **Sort order:** Revenue DESC
- **Naming convention:**

## Deployment Instructions (AWS Glue)

### 1. Upload the script to S3
```bash aws s3 cp search_keyword_performance_glue.py \ s3://ad-glue-artifacts/jobs/search_keyword_performance_glue.py```

---

## Configure the Glue Job
## Job name: e.g. search-keyword-performance
Type: Spark
Glue version: 4.0 or 5.0
Script location:
s3://ad-glue-artifacts/jobs/search_keyword_performance_glue.py
Job parameters (add exactly these):

--INPUT_FILE         s3://ad-raw-artifacts/input/dt=23-01-2026/data.csv
--OUTPUT_BASE_PATH   s3://ad-processed-artifacts/results/

Worker type: G.1X (cost-effective for demo)
Number of workers: 2–5
Job timeout: 60 minutes

##3. Run the job
Click Run job
Wait 1–10 minutes

##4. Where to find the output
After successful run, check this exact path:
s3://ad-processed-artifacts/results/2026-01-24_SearchKeywordPerformance.tab/

Search Engine Domain	Search Keyword	Revenue
www.bing.com	Zune	250.00
www.google.com	Ipod	290.00

Debugging Common Issues
No output file in S3?

Check CloudWatch Logs (Glue run → Error logs link)
Search for: "Output records", "Rows to write", "No matching rows"
If "Output records: 0" → input file has no purchase events (event_list with "1") + valid external referrer

Confirm folder: Output is always inside a date-named subfolder (e.g. 2026-01-24_SearchKeywordPerformance.tab/)
Verify --OUTPUT_BASE_PATH ends with / in job parameters

Job succeeds but empty results?

Data may lack qualifying rows (purchase + search referrer)
Test with sample data (21 rows from assessment) — should produce 2 rows ($540 total)


