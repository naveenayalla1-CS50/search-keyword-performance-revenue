# Usage Examples

This document provides real-world usage scenarios for the Search Keyword Performance Revenue Pipeline.

## Table of Contents
1. [Basic Local Usage](#basic-local-usage)
2. [AWS Glue Deployment](#aws-glue-deployment)
3. [Sample Data Format](#sample-data-format)
4. [Output Format](#output-format)
5. [Performance Tuning](#performance-tuning)
6. [Troubleshooting](#troubleshooting)

---

## Basic Local Usage

### Scenario 1: Single File Processing (Development)

```python
from pyspark.sql import SparkSession
from app import SearchKeywordPerformanceApp
from config import JobConfig

# Create Spark session for local testing
spark = SparkSession.builder \
    .appName("SearchKeywordPerformance") \
    .master("local[4]") \
    .getOrCreate()

# Configure job
config = JobConfig(
    input_path="data/adobe_hits_sample.tsv",
    output_path="output/results",
    keyword_param="q",
    coalesce_files=1
)

# Run pipeline
app = SearchKeywordPerformanceApp(
    spark=spark,
    input_file=config.input_path,
    output_base_path=config.output_path
)
app.run()

# Output will be at: output/results/2024-06-01_SearchKeywordPerformance.tab
```

**Expected Output:**
```
Search Engine Domain    Search Keyword         Revenue
www.google.com         gaming laptop          52450.75
www.google.com         machine learning       41230.50
www.bing.com          python tutorial        28900.00
search.yahoo.com      data science course    15600.25
```

---

## AWS Glue Deployment

### Scenario 2: Production Glue Job with S3 Input/Output

#### Step 1: Create IAM Role with S3 Access

```bash
# Create role
aws iam create-role \
  --role-name GlueSearchKeywordPerformanceRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "glue.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Attach Glue service role policy
aws iam attach-role-policy \
  --role-name GlueSearchKeywordPerformanceRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole

# Attach S3 policy
aws iam put-role-policy \
  --role-name GlueSearchKeywordPerformanceRole \
  --policy-name GlueS3Access \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::analytics-data-bucket/*",
          "arn:aws:s3:::analytics-data-bucket"
        ]
      }
    ]
  }'
```

#### Step 2: Create Glue Job

```bash
aws glue create-job \
  --name search-keyword-performance-daily \
  --role arn:aws:iam::ACCOUNT_ID:role/GlueSearchKeywordPerformanceRole \
  --command '{"Name":"glueetl","ScriptLocation":"s3://code-bucket/search-keyword-performance/app.py"}' \
  --default-arguments '{
    "--TempDir": "s3://analytics-data-bucket/glue-temp",
    "--job-bookmark-option": "job-bookmark-enabled",
    "--job-language": "python",
    "--additional-python-modules": "pyspark==3.3.0"
  }'
```

#### Step 3: Upload Code to S3

```bash
aws s3 cp app.py s3://code-bucket/search-keyword-performance/
aws s3 cp config.py s3://code-bucket/search-keyword-performance/
aws s3 cp extractors.py s3://code-bucket/search-keyword-performance/
aws s3 cp transformations.py s3://code-bucket/search-keyword-performance/
aws s3 cp logging_utils.py s3://code-bucket/search-keyword-performance/
```

#### Step 4: Start Job with S3 Paths

```bash
aws glue start-job-run \
  --job-name search-keyword-performance-daily \
  --arguments '{
    "--INPUT_PATH": "s3://analytics-data-bucket/adobe-hits/2024-06-01/",
    "--OUTPUT_PATH": "s3://analytics-data-bucket/keyword-performance/"
  }'
```

#### Step 5: Monitor Job Execution

```bash
# Get job run status
aws glue get-job-run \
  --job-name search-keyword-performance-daily \
  --run-id jr_abc123

# View CloudWatch logs
aws logs tail /aws-glue/jobs/search-keyword-performance-daily --follow
```

#### Step 6: Schedule Daily Execution

```bash
# Create EventBridge rule for daily execution at 2 AM UTC
aws events put-rule \
  --name search-keyword-performance-daily-trigger \
  --schedule-expression "cron(0 2 * * ? *)" \
  --state ENABLED

# Add Glue job as target
aws events put-targets \
  --rule search-keyword-performance-daily-trigger \
  --targets "Id"="1","Arn"="arn:aws:glue:us-east-1:ACCOUNT_ID:job/search-keyword-performance-daily","RoleArn"="arn:aws:iam::ACCOUNT_ID:role/EventBridgeGlueRole","GlueParameters"='{"JobName":"search-keyword-performance-daily","Arguments":"{\"--INPUT_PATH\":\"s3://analytics-data-bucket/adobe-hits/{{date}}/\",\"--OUTPUT_PATH\":\"s3://analytics-data-bucket/keyword-performance/\"}"}'
```

---

## Sample Data Format

### Adobe Analytics Hit-Level Data (TSV)

Input file: `adobe_hits_sample.tsv`

```
hit_id	referrer	event_list	product_list
1	https://www.google.com/search?q=gaming+laptop	21,1,22	GamingLaptop;Electronics;1;1299.99
2	https://www.google.com/search?q=gaming+laptop	21,1,22	ExternalMousePad;Accessories;1;25.00,GamingKeyboard;Accessories;1;89.99
3	https://direct.website.com/homepage	22,30	None
4	https://search.yahoo.com/search?p=python+tutorial	1,22	PythonCourse;Training;1;99.00
5	https://www.bing.com/search?q=machine+learning	21	MachineLearnBook;Books;2;39.99
6	https://www.google.com/search?q=gaming+laptop	1,22	MonitorUltra;Electronics;1;499.99
```

### Field Descriptions

- **hit_id**: Unique hit identifier from Adobe
- **referrer**: Full referrer URL (from where the user clicked to site)
- **event_list**: Comma-separated Adobe event IDs (1=purchase, others=engagement events)
- **product_list**: Semicolon/comma-delimited product data:
  - Format: `productName;category;quantity;revenue`
  - Multiple products separated by commas
  - Used for revenue attribution

---

## Output Format

### Result File: `2024-06-01_SearchKeywordPerformance.tab`

Tab-delimited output with formatted revenue:

```
Search Engine Domain	Search Keyword	Revenue
www.google.com	gaming laptop	1814.98
www.google.com	machine learning	39999.00
search.yahoo.com	python tutorial	99.00
www.bing.com	machine learning	79.98
```

### Output Column Definitions

- **Search Engine Domain**: Normalized search engine domain (www.google.com, search.yahoo.com, etc.)
- **Search Keyword**: Decoded search query from the referrer URL
- **Revenue**: Total revenue (sum across all purchase transactions) for that (domain, keyword) pair, formatted to 2 decimal places

---

## Performance Tuning

### Scenario 3: Large-Scale Processing (100M+ Records)

For processing very large datasets on AWS Glue:

```bash
# Create job with optimized settings for large data
aws glue create-job \
  --name search-keyword-performance-large-scale \
  --role arn:aws:iam::ACCOUNT_ID:role/GlueSearchKeywordPerformanceRole \
  --command '{"Name":"gluetl","ScriptLocation":"s3://code-bucket/search-keyword-performance/app.py"}' \
  --max-capacity 10 \
  --glue-version "4.0" \
  --default-arguments '{
    "--TempDir": "s3://analytics-data-bucket/glue-temp",
    "--job-bookmark-option": "job-bookmark-enabled",
    "--job-language": "python",
    "--enable-spark-ui": "true",
    "--spark-event-logs-path": "s3://analytics-data-bucket/spark-logs/",
    "--enable-glue-datacatalog": "true"
  }'

# Run with input partitioning
aws glue start-job-run \
  --job-name search-keyword-performance-large-scale \
  --arguments '{
    "--INPUT_PATH": "s3://analytics-data-bucket/adobe-hits/2024-06-01/",
    "--OUTPUT_PATH": "s3://analytics-data-bucket/keyword-performance/",
    "--COALESCE_FILES": "4"
  }'
```

**Performance Tips:**
1. Use `--COALESCE_FILES 4` instead of 1 for 100M+ records (reduces executor memory usage)
2. Enable job bookmarks for incremental processing
3. Use Glue DPU allocation (max-capacity) based on data volume
4. Monitor Spark UI in CloudWatch for bottlenecks

### Scenario 4: Incremental Daily Processing

Using Glue job bookmarks to process only new data:

```python
# In your Glue job script, use job bookmark
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'INPUT_PATH', 'OUTPUT_PATH'])

glueContext = GlueContext(SparkContext.getOrCreate())
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Glue will automatically track processed files with job bookmarks
df = glueContext.create_dynamic_frame.from_options(
    "s3",
    {
        "paths": [args['INPUT_PATH']],
        "recurse": True
    },
    format="csv",
    format_options={
        "withHeader": True,
        "separator": "\t"
    }
)

# ... process DataFrame ...

job.commit()  # Commits bookmark state
```

---

## Troubleshooting

### Issue 1: Job Fails with "No such file or directory"

**Cause:** Input path doesn't exist or permissions issue

**Solution:**
```bash
# Verify S3 path exists and is readable
aws s3 ls s3://analytics-data-bucket/adobe-hits/2024-06-01/

# Check IAM role has S3 permissions
aws iam get-role-policy \
  --role-name GlueSearchKeywordPerformanceRole \
  --policy-name GlueS3Access
```

### Issue 2: Job Times Out (> 60 minutes)

**Cause:** Processing too much data with insufficient Glue DPU allocation

**Solution:**
```bash
# Increase max-capacity for the Glue job
aws glue update-job \
  --name search-keyword-performance-daily \
  --max-capacity 25  # Increase from default

# Or reduce data by filtering for recent dates only
--INPUT_PATH s3://bucket/adobe-hits/2024-06-01/  # Single day instead of month
```

### Issue 3: Low Revenue Values or Missing Data

**Cause:** Filters are too strict or referrer format differs

**Debugging:**
```python
# In your Spark session, add debugging output
result_df.filter(F.col("Search Engine Domain").isNull()).show(100)  # Find nulls
result_df.filter(F.col("Revenue") == 0.0).show(100)  # Find zero revenue

# Check raw data transformations
enriched_df.select("referrer", "Search Keyword", "Revenue").show(100)
```

### Issue 4: Revenue Totals Don't Match Expected Numbers

**Cause:** Revenue might be attributed to multiple keywords from single transaction

**Note:** This pipeline correctly attributes 100% revenue to each product's referring keyword. If a user came from keyword A but purchased via keyword B on same day, revenue is split.

---

## Monitoring & Alerting

### CloudWatch Dashboard

```bash
# Create dashboard for job monitoring
aws cloudwatch put-dashboard \
  --dashboard-name SearchKeywordPerformance \
  --dashboard-body file://dashboard-config.json
```

Example `dashboard-config.json`:
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/Glue", "glue.driver.aggregate.numFailedTasks", {"stat": "Sum"}],
          ["AWS/Glue", "glue.driver.aggregate.numCompletedTasks", {"stat": "Sum"}],
          ["AWS/Glue", "glue.executors.totalTime", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Glue Job Execution Metrics"
      }
    }
  ]
}
```

### CloudWatch Alarms

```bash
# Alert if job fails
aws cloudwatch put-metric-alarm \
  --alarm-name search-keyword-performance-job-failure \
  --alarm-description "Alert when keyword performance job fails" \
  --metric-name glue:num-failed-tasks \
  --namespace AWS/Glue \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT_ID:AlertTopic
```

---

## Advanced: Custom Parameter Configuration

If you need to extend the pipeline for additional search engines:

```python
# Extend extractors.py
SEARCH_ENGINE_PARAMS = {
    "google.com": "q",
    "www.google.com": "q",
    "bing.com": "q",
    "www.bing.com": "q",
    "yandex.com": "text",  # Yandex uses 'text' parameter
    "baidu.com": "wd",     # Baidu uses 'wd' parameter
}

def extract_search_keyword_custom(referrer: str) -> Optional[str]:
    """Extended to support additional search engines."""
    # ... implementation using SEARCH_ENGINE_PARAMS ...
```

---

## Questions?

For issues, questions, or feature requests, please open an issue on GitHub or contact the development team.
