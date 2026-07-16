import json
import logging
import os
from google.cloud import storage
from config import PROJECT_ID, BUCKET_NAME

logger = logging.getLogger(__name__)

class StorageClient:
    def __init__(self):
        self.client = storage.Client(project=PROJECT_ID)
        self.bucket = self.client.bucket(BUCKET_NAME)
        logger.info(f"✅ GCS connecté → gs://{BUCKET_NAME}")

    def upload_file(self, local_path: str, gcs_path: str) -> bool:
        try:
            blob    = self.bucket.blob(gcs_path)
            size_mb = os.path.getsize(local_path) / (1024 * 1024)
            blob.upload_from_filename(local_path)
            logger.info(f"📤 {local_path} → gs://{BUCKET_NAME}/{gcs_path} ({size_mb:.1f} MB)")
            return True
        except Exception as e:
            logger.error(f"❌ Upload échoué {local_path} : {e}")
            return False

    def upload_json(self, data: dict | list, gcs_path: str) -> bool:
        try:
            blob = self.bucket.blob(gcs_path)
            blob.upload_from_string(
                data=json.dumps(data, indent=2, ensure_ascii=False),
                content_type="application/json"
            )
            logger.info(f"📤 JSON → gs://{BUCKET_NAME}/{gcs_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Upload JSON échoué : {e}")
            return False

    def list_files(self, prefix: str) -> list:
        blobs = self.client.list_blobs(BUCKET_NAME, prefix=prefix)
        return [blob.name for blob in blobs]