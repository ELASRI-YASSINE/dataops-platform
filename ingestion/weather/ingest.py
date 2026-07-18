# ingestion/weather/ingest.py
import requests
from datetime import datetime
from ingestion.base.connector import BaseConnector
from ingestion.base.uploader import GCSUploader
from config.constants import BRAZILIAN_CITIES, WEATHER_BASE_URL, GCSPaths
from config.settings import settings
from common.utils import get_timestamp

class WeatherConnector(BaseConnector):
    """Connecteur pour l'API OpenWeatherMap"""

    def __init__(self):
        super().__init__()
        self.uploader = GCSUploader()

    def _fetch_city(self, city: str) -> dict | None:
        try:
            r = requests.get(
                f"{WEATHER_BASE_URL}/weather",
                params={
                    "q"     : f"{city},BR",
                    "appid" : settings.WEATHER_API_KEY,
                    "units" : "metric",
                    "lang"  : "fr"
                },
                timeout=10
            )
            r.raise_for_status()
            raw = r.json()
            return {
                "city"        : city,
                "temperature" : raw["main"]["temp"],
                "humidity"    : raw["main"]["humidity"],
                "condition"   : raw["weather"][0]["description"],
                "wind_speed"  : raw["wind"]["speed"],
                "latitude"    : raw["coord"]["lat"],
                "longitude"   : raw["coord"]["lon"],
                "timestamp"   : datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error(f"❌ {city} : {e}")
            return None

    def extract(self) -> list:
        self.logger.info(f"📡 Météo pour {len(BRAZILIAN_CITIES)} villes...")
        results = []
        for city in BRAZILIAN_CITIES:
            weather = self._fetch_city(city)
            if weather:
                results.append(weather)
                self.logger.info(
                    f"   ✅ {city:<20} "
                    f"{weather['temperature']:>5.1f}°C  "
                    f"{weather['condition']}"
                )
        return results

    def validate(self, data: list) -> bool:
        if not data:
            self.logger.error("❌ Aucune donnée météo reçue")
            return False
        self.logger.info(f"✅ {len(data)}/{len(BRAZILIAN_CITIES)} villes récupérées")
        return True

    def load(self, data: list) -> bool:
        gcs_path = f"{GCSPaths.RAW_WEATHER}/weather_{get_timestamp()}.json"
        return self.uploader.upload_json({
            "timestamp" : datetime.utcnow().isoformat(),
            "count"     : len(data),
            "cities"    : data,
            "source"    : "openweathermap.org"
        }, gcs_path)
