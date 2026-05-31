# web analytics hit-level data

## Project Summary

This project implements a cloud-based ETL pipeline for analyzing Adobe Analytics hit-level data and identifying revenue generated from external search engine traffic.

The pipeline processes raw tab-separated hit-level data, filters purchase events, extracts search engine domains and search keywords from referrer URLs, parses revenue from product-level fields, and produces a revenue-ranked output file for business reporting.

## Business Problem

Marketing and analytics teams often need to understand which external search engines and search keywords contribute to revenue. This project answers the following business question:

**How much revenue comes from external search engines such as Google, Yahoo, and MSN/Bing, and which search keywords perform best?**

## Required Output

The pipeline generates a tab-delimited file using the following naming convention:

```text
YYYY-mm-dd_SearchKeywordPerformance.tab
```

Output columns:

```text
Search Engine Domain
Search Keyword
Revenue
```

The output is sorted by revenue in descending order.

## Solution Overview

Key features:

* Reads Adobe Analytics hit-level TSV data from Amazon S3
* Filters purchase events where `event_list` contains event `1`
* Extracts external search engine domains from referrer URLs
* Extracts search keywords from referrer query parameters
* Parses revenue from the `product_list` field
* Aggregates total revenue by search engine domain and keyword
* Writes a sorted tab-delimited output file to Amazon S3
* Includes AWS Glue deployment instructions
* Includes Terraform infrastructure examples for cloud deployment

## Technology Stack

* Apache Spark / PySpark
* AWS Glue
* Amazon S3
* Amazon CloudWatch Logs and Metrics
* Terraform for infrastructure as code
* Python
* Shell scripting

## Data Engineering Concepts Demonstrated

* Batch ETL pipeline design
* Cloud-based data processing
* PySpark transformations
* Search referrer parsing
* Revenue aggregation logic
* S3-based data lake input and output
* AWS Glue job configuration
* Infrastructure as code with Terraform
* Data validation and debugging
* CloudWatch monitoring and troubleshooting

## Data Processing Logic

### Input

Source: Adobe Analytics hit-level data in TSV format
Location: Amazon S3

Key columns used:

* `event_list`
* `referrer`
* `product_list`

### Transformations

1. Filter rows where `event_list` contains purchase event `1`
2. Extract external search engine domain from `referrer`
3. Extract search keyword from referrer query parameters
4. Parse revenue from `product_list`
5. Aggregate total revenue by `Search Engine Domain` and `Search Keyword`
6. Sort results by revenue in descending order

### Output

Format: Tab-separated `.tab` file
Header: Included
Sort order: Revenue descending

Example output:

```text
Search Engine Domain    Search Keyword    Revenue
www.google.com          Ipod              290.00
www.bing.com            Zune              250.00
```

## Business Value

This pipeline helps marketing and analytics teams identify which external search keywords generate revenue. The output can support:

* Search attribution analysis
* Campaign optimization
* Revenue-focused reporting
* Marketing performance analysis
* Data-driven decision making

## Deployment Instructions for AWS Glue

### 1. Upload the script to S3

```bash
aws s3 cp search_keyword_performance_glue.py s3://ad-glue-artifacts/jobs/search_keyword_performance_glue.py
```

### 2. Configure the AWS Glue Job

Example job name:

```text
search-keyword-performance
```

Recommended configuration:

```text
Type: Spark
Glue version: 4.0 or 5.0
Worker type: G.1X
Number of workers: 2-5
Job timeout: 60 minutes
```

Script location:

```text
s3://ad-glue-artifacts/jobs/search_keyword_performance_glue.py
```

Job parameters:

```text
--INPUT_FILE         s3://ad-raw-artifacts/input/dt=23-01-2026/data.csv
--OUTPUT_BASE_PATH   s3://ad-processed-artifacts/results/
```

### 3. Run the Job

Start the AWS Glue job from the AWS Console or CLI. For small sample data, the job should complete within a few minutes.

### 4. Find the Output

After a successful run, output will be written to a date-named folder such as:

```text
s3://ad-processed-artifacts/results/2026-01-24_SearchKeywordPerformance.tab/
```

## Debugging Common Issues

### No output file in S3

Check AWS CloudWatch Logs from the Glue job run and search for:

```text
Output records
Rows to write
No matching rows
```

If output records are `0`, verify that the input file contains:

* Purchase events where `event_list` includes `1`
* Valid external search engine referrers
* Valid revenue values in `product_list`

### Job succeeds but results are empty

Possible causes:

* Input data does not contain qualifying purchase events
* Referrer URLs are missing or not from supported search engines
* Search keywords are missing from query parameters
* Revenue values are missing or malformed

### Output path issue

Confirm that `--OUTPUT_BASE_PATH` ends with `/`.

Example:

```text
s3://ad-processed-artifacts/results/
```

## Example Test Case

Using the sample assessment dataset, the expected output includes two revenue-producing search keyword records with a total revenue of `$540.00`.

## Suggested Future Enhancements

* Add data quality checks for required columns
* Add automated unit tests for revenue parsing logic
* Add CI workflow for test execution
* Add support for additional search engines
* Add dashboard output for marketing analytics
* Add Snowflake or BigQuery implementation
* Add architecture diagram
* Add sample CloudWatch log output

## Author

Naveen Ayalla
Data Engineer
