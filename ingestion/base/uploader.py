from google.cloud import storage

from config.settings import settings
from common.logger import logger


class GCSUploader:

    def __init__(self):

        self.client = storage.Client(
            project=settings.PROJECT_ID
        )

        self.bucket = self.client.bucket(
            settings.BUCKET_NAME
        )

        logger.info(
            f"Connected to bucket : {settings.BUCKET_NAME}"
        )
