from dataclasses import dataclass
from dotenv import load_dotenv
import os

# Charge le fichier .env
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Configuration globale du projet.
    Toutes les variables viennent du fichier .env.
    """

    # GCP
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    BUCKET_NAME: str = os.getenv("GCP_BUCKET_NAME", "")
    REGION: str = os.getenv("GCP_REGION", "")

    # APIs
    WEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    EXCHANGE_API_KEY: str = os.getenv("EXCHANGE_RATE_API_KEY", "")

    # Kaggle
    KAGGLE_USERNAME: str = os.getenv("KAGGLE_USERNAME", "")
    KAGGLE_KEY: str = os.getenv("KAGGLE_KEY", "")


settings = Settings()
