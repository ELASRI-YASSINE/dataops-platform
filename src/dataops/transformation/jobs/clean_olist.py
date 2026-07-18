from dataops.transformation.spark.session import SparkManager
from dataops.transformation.spark.reader import SparkReader
from dataops.transformation.spark.writer import SparkWriter
from dataops.transformation.spark.transformer import DataTransformer
from dataops.transformation.spark.validator import DataValidator

INPUT = "gs://dataops-pfa-datalake/raw/olist/orders/olist_orders_dataset.csv"

OUTPUT = "gs://dataops-pfa-datalake/processed/olist/orders/"


spark = SparkManager.create()

reader = SparkReader(spark)

df = reader.csv(INPUT)

df = DataTransformer.clean(df)

DataValidator.validate(df)

SparkWriter.parquet(df, OUTPUT)

print("Job terminé.")
