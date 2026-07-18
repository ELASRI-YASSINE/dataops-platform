# ingestion/olist/ingest.py
import os
import time
import pandas as pd
from datetime import datetime
from ingestion.base.connector import BaseConnector
from ingestion.base.uploader import GCSUploader
from config.constants import OLIST_FILES, GCSPaths
from config.settings import settings
from common.utils import file_size_mb

class OlistConnector(BaseConnector):
    """Connecteur pour le dataset Olist e-commerce"""

    def __init__(self, data_folder: str = None):
        super().__init__()
        self.data_folder = data_folder or settings.DATA_FOLDER
        self.uploader    = GCSUploader()
        self.stats       = []

    def extract(self) -> dict:
        """Vérifie et charge les métadonnées des CSV Olist"""
        self.logger.info(f"📂 Lecture depuis : {self.data_folder}")
        files_found = {}

        for filename, table_name in OLIST_FILES.items():
            path = os.path.join(self.data_folder, filename)
            if os.path.exists(path):
                files_found[filename] = {
                    "path"       : path,
                    "table_name" : table_name,
                    "size_mb"    : file_size_mb(path)
                }
                self.logger.info(f"  ✅ {table_name:<15} {file_size_mb(path):.1f} MB")
            else:
                self.logger.warning(f"  ⚠️  {filename} introuvable")

        return files_found

    def validate(self, data: dict) -> bool:
        """Valide que les fichiers essentiels sont présents"""
        required = ["olist_orders_dataset.csv", "olist_customers_dataset.csv"]
        for req in required:
            if req not in data:
                self.logger.error(f"❌ Fichier requis manquant : {req}")
                return False

        for filename, info in data.items():
            df       = pd.read_csv(info["path"], nrows=100)
            null_pct = round(df.isnull().mean().mean() * 100, 2)
            self.stats.append({
                "table"    : info["table_name"],
                "size_mb"  : info["size_mb"],
                "columns"  : list(df.columns),
                "null_pct" : null_pct
            })
            self.logger.info(
                f"  📊 {info['table_name']:<15} "
                f"{len(df.columns)} cols | "
                f"{null_pct}% nulls"
            )
        return True

    def load(self, data: dict) -> bool:
        """Upload chaque CSV vers GCS raw/olist/ — skip si déjà uploadé"""
        success = 0
        skipped = 0

        for filename, info in data.items():
            gcs_path = f"{GCSPaths.RAW_OLIST}/{info['table_name']}/{filename}"

            # Skip si déjà uploadé
            if self.uploader.file_exists(gcs_path):
                self.logger.info(f"⏭️  Déjà uploadé : {info['table_name']}")
                skipped += 1
                success += 1
                continue

            self.uploader.upload_file(info["path"], gcs_path)
            success += 1

        # Sauvegarde les stats
        self.uploader.upload_json({
            "ingestion_timestamp" : datetime.utcnow().isoformat(),
            "tables"              : self.stats
        }, f"{GCSPaths.RAW_OLIST}/metadata/ingestion_report.json")

        self.logger.info(
            f"✅ {success}/{len(data)} tables | "
            f"{skipped} déjà présentes"
        )
        return True
