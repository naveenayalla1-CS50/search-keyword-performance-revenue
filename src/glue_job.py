import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from app import SearchKeywordPerformanceApp

# Glue passes args as: --INPUT_FILE=s3://...
args = dict(arg.split("=") for arg in sys.argv[1:])
input_file = args["--INPUT_FILE"]

OUTPUT_BASE_PATH = "s3://your-output-bucket/output"

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init("SearchKeywordPerformance", sys.argv)

app = SearchKeywordPerformanceApp(
    spark=spark,
    input_file=input_file,
    output_base_path=OUTPUT_BASE_PATH
)

app.run()
job.commit()
