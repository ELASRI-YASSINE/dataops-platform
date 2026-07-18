from dataops.warehouse.client import BigQueryClient
from dataops.warehouse.loader import BigQueryLoader
from dataops.warehouse.schema import WarehouseSchema
from dataops.warehouse.bronze_tables import BRONZE_TABLES


class WarehouseManager:

    def __init__(self):
        self.client = BigQueryClient.create()
        self.schema = WarehouseSchema(self.client)
        self.loader = BigQueryLoader(self.client)

    def initialize(self):
        self.schema.create_dataset()

    def load(self, source_uri, table):
        self.loader.load_parquet(
            source_uri=source_uri,
            table_name=table
        )

    def load_all_bronze(self):

        for table in BRONZE_TABLES:

            print("=" * 60)
            print(f"Loading {table['table']}")
            print("=" * 60)

            self.loader.load_parquet(
                source_uri=table["source"],
                table_name=table["table"]
            )
