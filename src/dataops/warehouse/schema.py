from google.cloud import bigquery

from dataops.warehouse.config import DATASET
from dataops.warehouse.config import LOCATION


class WarehouseSchema:

    def __init__(self, client):

        self.client = client

    def create_dataset(self):

        dataset_id = f"{self.client.project}.{DATASET}"

        dataset = bigquery.Dataset(dataset_id)

        dataset.location = LOCATION

        dataset = self.client.create_dataset(
            dataset,
            exists_ok=True
        )

        print(f"Dataset ready : {dataset.dataset_id}")
