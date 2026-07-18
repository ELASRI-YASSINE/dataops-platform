from pyspark.sql import SparkSession


class SparkManager:

    @staticmethod
    def create():

        spark = (
            SparkSession.builder
            .appName("DataOps Platform")
            .getOrCreate()
        )

        return spark
