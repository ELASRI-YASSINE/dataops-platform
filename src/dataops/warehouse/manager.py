from dataops.warehouse.client import BigQueryClient
from dataops.warehouse.loader import BigQueryLoader
from dataops.warehouse.schema import WarehouseSchema


class WarehouseManager:

    def __init__(self):

        self.client = BigQueryClient.create()

        self.schema = WarehouseSchema(self.client)

        self.loader = BigQueryLoader(self.client)

    def initialize(self):

        self.schema.create_dataset()

    def load(self, source_uri, table):

        self.loader.load_parquet(

            source_uri,

            table

        )
