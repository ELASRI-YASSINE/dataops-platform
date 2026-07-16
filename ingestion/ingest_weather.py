import logging
import requests
from datetime import datetime
from storage_client import StorageClient
from config import (
    WEATHER_API_KEY, WEATHER_BASE_URL,
    BRAZILIAN_CITIES, GCS_RAW_WEATHER
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_city(city: str) -> dict | None:
    try:
        response = requests.get(
            f"{WEATHER_BASE_URL}/weather",
            params={
                "q"     : f"{city},BR",
                "appid" : WEATHER_API_KEY,
                "units" : "metric",
                "lang"  : "fr"
            },
            timeout=10
        )
        response.raise_for_status()
        raw = response.json()

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
        logger.error(f"❌ {city} : {e}")
        return None


def run():
    logger.info("🚀 INGESTION WEATHER DATA")
    gcs     = StorageClient()
    results = []

    for city in BRAZILIAN_CITIES:
        weather = fetch_city(city)
        if weather:
            results.append(weather)
            logger.info(
                f"✅ {city:<20} "
                f"{weather['temperature']:>5.1f}°C  "
                f"{weather['condition']}"
            )

    today    = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    gcs_path = f"{GCS_RAW_WEATHER}/weather_{today}.json"
    gcs.upload_json({
        "timestamp" : datetime.utcnow().isoformat(),
        "count"     : len(results),
        "cities"    : results
    }, gcs_path)

    logger.info(f"✅ {len(results)} villes → {gcs_path}")
    return results


if __name__ == "__main__":
    run()