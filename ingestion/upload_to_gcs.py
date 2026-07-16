import logging
import os
import pandas as pd
from datetime import datetime
from storage_client import StorageClient
from config import OLIST_FILES, GCS_RAW_OLIST

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def validate_csv(filepath: str, table_name: str) -> dict:
    df = pd.read_csv(filepath, nrows=1000)
    stats = {
        "table"    : table_name,
        "columns"  : list(df.columns),
        "null_pct" : round(df.isnull().mean().mean() * 100, 2),
        "size_mb"  : round(os.path.getsize(filepath) / (1024*1024), 2)
    }
    logger.info(
        f"   📊 {table_name:<15} "
        f"{stats['size_mb']:>6.1f} MB | "
        f"{len(df.columns)} cols | "
        f"{stats['null_pct']}% nulls"
    )
    return stats


def upload_olist(data_folder: str = "data/") -> dict:
    logger.info("=" * 55)
    logger.info("🚀 INGESTION OLIST DATASET")
    logger.info("=" * 55)

    gcs    = StorageClient()
    report = {"success": [], "failed": [], "stats": []}

    for filename, table_name in OLIST_FILES.items():
        local_path = os.path.join(data_folder, filename)
        gcs_path   = f"{GCS_RAW_OLIST}/{table_name}/{filename}"

        logger.info(f"\n── {table_name.upper()}")

        if not os.path.exists(local_path):
            logger.warning(f"⚠️  Introuvable : {local_path}")
            report["failed"].append(table_name)
            continue

        stats = validate_csv(local_path, table_name)
        report["stats"].append(stats)

        if gcs.upload_file(local_path, gcs_path):
            report["success"].append(table_name)
        else:
            report["failed"].append(table_name)

    total_mb = sum(s["size_mb"] for s in report["stats"])
    logger.info(f"\n✅ {len(report['success'])} tables uploadées")
    logger.info(f"💾 Total : {total_mb:.1f} MB")
    return report


if __name__ == "__main__":
    upload_olist("data/")