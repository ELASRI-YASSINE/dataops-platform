from pyspark.sql import DataFrame


class SparkWriter:

    @staticmethod
    def parquet(df: DataFrame, path: str):

        (
            df.write
            .mode("overwrite")
            .parquet(path)
        )
