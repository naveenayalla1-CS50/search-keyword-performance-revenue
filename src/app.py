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
        self.logger.info(f"Processing input file: {self.input_file}")

        df = (
            self.spark.read
            .option("header", True)
            .option("escape", "\"")
            .csv(self.input_file)
        )

        input_count = df.count()
        self.logger.info(f"Input records: {input_count}")

        result_df = build_keyword_performance_df(df)

        output_count = result_df.count()
        self.logger.info(f"Output records: {output_count}")

        run_date = datetime.utcnow().strftime("%Y-%m-%d")
        output_file = f"{run_date}_SearchKeywordPerformance.tab"

        (
            result_df
            .coalesce(1)
            .write
            .mode("overwrite")
            .option("delimiter", "\t")
            .option("header", True)
            .csv(f"{self.output_base_path}/{output_file}")
        )

        self.logger.info("Job completed successfully")
