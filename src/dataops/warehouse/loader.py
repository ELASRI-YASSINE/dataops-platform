from google.cloud import bigquery

from dataops.warehouse.config import DATASET
from dataops.warehouse.config import WRITE_DISPOSITION


class BigQueryLoader:

    def __init__(self, client):

        self.client = client

    def load_parquet(
        self,
        source_uri,
        table_name
    ):

        table_id = f"{self.client.project}.{DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(

            source_format=bigquery.SourceFormat.PARQUET,

            autodetect=True,

            write_disposition=WRITE_DISPOSITION

        )

        load_job = self.client.load_table_from_uri(

            source_uri,

            table_id,

            job_config=job_config

        )

        load_job.result()

        table = self.client.get_table(table_id)

        print("=" * 60)

        print("TABLE :", table.table_id)

        print("ROWS :", table.num_rows)

        print("=" * 60)
