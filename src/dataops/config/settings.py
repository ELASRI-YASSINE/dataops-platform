# config/settings.py
"""
Charge toutes les variables d'environnement depuis .env
Point d'entrée unique pour la configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GCP
    GCP_PROJECT_ID  : str = os.getenv("GCP_PROJECT_ID",  "dataops-pfa-502611")
    GCP_BUCKET_NAME : str = os.getenv("GCP_BUCKET_NAME", "dataops-pfa-datalake")
    GCP_REGION      : str = os.getenv("GCP_REGION",      "europe-west1")
    BQ_DATASET_ID   : str = os.getenv("BQ_DATASET_ID",   "dataops_warehouse")

    # APIs
    EXCHANGE_API_KEY : str = os.getenv("EXCHANGE_RATE_API_KEY", "")
    WEATHER_API_KEY  : str = os.getenv("OPENWEATHER_API_KEY",   "")

    # Paths
    DATA_FOLDER : str = os.getenv("DATA_FOLDER", "data/")
    LOGS_FOLDER : str = os.getenv("LOGS_FOLDER", "logs/")

settings = Settings()
