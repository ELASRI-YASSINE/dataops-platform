from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp


class DataTransformer:
    """
    Generic Spark transformations.
    """

    @staticmethod
    def clean(df: DataFrame) -> DataFrame:
        """
        Basic cleaning:
        - remove duplicates
        - remove null rows
        - add ingestion timestamp
        """

        return (
            df
            .dropDuplicates()
            .na.drop()
            .withColumn(
                "ingestion_timestamp",
                current_timestamp()
            )
        )
