# ingestion/base/uploader.py
import json
import os
import time
from google.cloud import storage
from common.logger import get_logger
from common.exceptions import StorageError
from config.settings import settings

logger = get_logger(__name__)

class GCSUploader:
    """Client Google Cloud Storage centralisé"""

    def __init__(self):
        self.client = storage.Client(project=settings.GCP_PROJECT_ID)
        self.bucket = self.client.bucket(settings.GCP_BUCKET_NAME)
        logger.info(f"✅ GCS connecté → gs://{settings.GCP_BUCKET_NAME}")

    def upload_file(self, local_path: str, gcs_path: str, retries: int = 3) -> bool:
        """Upload un fichier local vers GCS avec retry automatique"""
        size_mb = os.path.getsize(local_path) / (1024 * 1024)

        for attempt in range(1, retries + 1):
            try:
                blob    = self.bucket.blob(gcs_path)
                timeout = max(300, int(size_mb * 10))
                blob.upload_from_filename(local_path, timeout=timeout)
                logger.info(
                    f"📤 {os.path.basename(local_path)} → "
                    f"gs://{settings.GCP_BUCKET_NAME}/{gcs_path} "
                    f"({size_mb:.1f} MB)"
                )
                return True
            except Exception as e:
                logger.warning(f"⚠️  Tentative {attempt}/{retries} : {e}")
                if attempt < retries:
                    wait = attempt * 10
                    logger.info(f"   ⏳ Retry dans {wait}s...")
                    time.sleep(wait)
                else:
                    raise StorageError(f"Upload échoué après {retries} tentatives : {local_path}")

    def upload_json(self, data: dict | list, gcs_path: str) -> bool:
        """Upload un dict Python directement en JSON vers GCS"""
        try:
            blob = self.bucket.blob(gcs_path)
            blob.upload_from_string(
                data=json.dumps(data, indent=2, ensure_ascii=False),
                content_type="application/json"
            )
            logger.info(f"📤 JSON → gs://{settings.GCP_BUCKET_NAME}/{gcs_path}")
            return True
        except Exception as e:
            raise StorageError(f"Upload JSON échoué : {e}")

    def file_exists(self, gcs_path: str) -> bool:
        """Vérifie si un fichier existe dans GCS"""
        return self.bucket.blob(gcs_path).exists()

    def list_files(self, prefix: str) -> list:
        """Liste les fichiers dans un dossier GCS"""
        blobs = self.client.list_blobs(settings.GCP_BUCKET_NAME, prefix=prefix)
        return [b.name for b in blobs]
