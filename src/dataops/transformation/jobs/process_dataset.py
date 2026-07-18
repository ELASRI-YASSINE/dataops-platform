from dataops.transformation.spark.session import SparkManager
from dataops.transformation.spark.reader import SparkReader
from dataops.transformation.spark.writer import SparkWriter
from dataops.transformation.spark.transformer import DataTransformer
from dataops.transformation.spark.validator import DataValidator


class DatasetProcessor:
    """
    Generic processor for any dataset.

    Steps:
        1. Read data
        2. Clean data
        3. Validate data
        4. Write Parquet
    """

    def __init__(self):
        self.spark = SparkManager.create()
        self.reader = SparkReader(self.spark)

    def process(self, input_path: str, output_path: str):

        print("=" * 60)
        print(f"Processing dataset")
        print(f"Input : {input_path}")
        print(f"Output: {output_path}")
        print("=" * 60)

        # -------------------------
        # Read
        # -------------------------
        df = self.reader.csv(input_path)

        # -------------------------
        # Transform
        # -------------------------
        df = DataTransformer.clean(df)

        # -------------------------
        # Validate
        # -------------------------
        DataValidator.validate(df)

        # -------------------------
        # Write
        # -------------------------
        SparkWriter.parquet(df, output_path)

        print("Dataset processed successfully.\n")

        return df
