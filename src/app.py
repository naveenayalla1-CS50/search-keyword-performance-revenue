from datetime import datetime
from pyspark.sql import SparkSession
from transformations import build_keyword_performance_df
from logging_utils import get_logger


class SearchKeywordPerformanceApp:
    """
    Entry point class for Search Keyword Performance processing.
    """
    def __init__(self, spark: SparkSession, input_file: str, output_base_path: str):
        self.spark = spark
        self.input_file = input_file
        self.output_base_path = output_base_path
        self.logger = get_logger(self.__class__.__name__)

    def run(self):
        self.logger.info(f"Starting processing of input file: {self.input_file}")

        # Read the TSV file (Adobe hit-level data)
        df = (
            self.spark.read
            .option("header", True)
            .option("delimiter", "\t")
            .option("escape", "\"")
            .option("multiLine", "true")           # handles multi-line quoted fields
            .option("inferSchema", "true")         # useful for local testing
            .csv(self.input_file)
        )

        input_count = df.count()
        self.logger.info(f"Input records loaded: {input_count:,}")

        # Apply business transformations
        result_df = build_keyword_performance_df(df)

        output_count = result_df.count()
        self.logger.info(f"Result records after transformation: {output_count:,}")

        # Generate output filename with run date
        run_date = datetime.utcnow().strftime("%Y-%m-%d")
        output_file = f"{run_date}_SearchKeywordPerformance.tab"

        # Write single tab-delimited file with header
        (
            result_df
            .coalesce(1)                        # single file output
            .write
            .mode("overwrite")
            .option("delimiter", "\t")
            .option("header", True)
            .option("emptyValue", "")           # clean empty cells
            .csv(f"{self.output_base_path}/{output_file}")
        )

        self.logger.info(f"Job completed successfully. Output written to: {self.output_base_path}/{output_file}")
