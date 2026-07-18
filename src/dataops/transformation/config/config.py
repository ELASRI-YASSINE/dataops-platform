import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "europe-west1")

BUCKET = os.getenv("GCP_BUCKET_NAME")

RAW_PATH = f"gs://{BUCKET}/raw"
PROCESSED_PATH = f"gs://{BUCKET}/processed"
