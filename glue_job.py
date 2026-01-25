"""
AWS Glue PySpark Job: Search Keyword Performance from Adobe Analytics Hit-Level Data

This job:
- Reads tab-delimited hit data from S3
- Processes it using SearchKeywordPerformanceApp
- Writes sorted tab-delimited output with date prefix
- Uses Glue context properly
"""

import sys, time

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

from pyspark.context import SparkContext

# Import your main application class
from app import SearchKeywordPerformanceApp


print("=== GLUE_JOB_PY_START ===", flush=True)
print("ARGV:", sys.argv, flush=True)
sys.stderr.write("=== STDERR_ALIVE ===\n")
sys.stderr.flush()
time.sleep(2)

# ------------------------------------------------------------------
# Parse job arguments – Glue standard way (recommended)
# ------------------------------------------------------------------
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'INPUT_FILE',           # e.g. --INPUT_FILE s3://my-bucket/hits.tsv
    'OUTPUT_BASE_PATH'      # e.g. --OUTPUT_BASE_PATH s3://my-bucket/results/
])

input_file = args['INPUT_FILE']
output_base_path = args['OUTPUT_BASE_PATH'].rstrip("/")  # clean trailing slash
print(f'Input file Path is {input_file}')

print(f'Output file Path is {output_base_path}')

# ------------------------------------------------------------------
# Initialize Glue context
# ------------------------------------------------------------------
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args['JOB_NAME'], args)

# ------------------------------------------------------------------
# Run the application
# ------------------------------------------------------------------
try:
    print('Job is getting started...')
    app = SearchKeywordPerformanceApp(
        spark=spark,
        input_file=input_file,
        output_base_path=output_base_path
    )
    app.run()

    print(f"Job succeeded. Output written to: {output_base_path}/<date>_SearchKeywordPerformance.tab")
    
except Exception as e:
    print(f"Job failed with error: {str(e)}")
    raise  # This will mark the Glue job as FAILED

# ------------------------------------------------------------------
# Commit the job
# ------------------------------------------------------------------
job.commit()
