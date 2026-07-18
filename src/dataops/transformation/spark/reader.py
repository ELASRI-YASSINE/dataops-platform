from pyspark.sql import SparkSession


class SparkReader:

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def csv(self, path: str):
        return (
            self.spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(path)
        )

    def parquet(self, path: str):
        return self.spark.read.parquet(path)

    def json(self, path: str):
        return self.spark.read.json(path)
