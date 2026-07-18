from pyspark.sql import DataFrame


class DataValidator:

    @staticmethod
    def validate(df: DataFrame):

        count = df.count()

        if count == 0:
            raise ValueError("Dataset is empty.")

        print("=" * 50)
        print("Validation OK")
        print(f"Rows : {count}")
        print("=" * 50)
