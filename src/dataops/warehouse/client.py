from google.cloud import bigquery

from dataops.warehouse.config import PROJECT_ID


class BigQueryClient:

    @staticmethod
    def create():

        return bigquery.Client(project=PROJECT_ID)
