import logging
import requests
from datetime import datetime
from storage_client import StorageClient
from config import (
    EXCHANGE_API_KEY, EXCHANGE_BASE_URL,
    BASE_CURRENCY, TARGET_CURRENCIES, GCS_RAW_EXCHANGE
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_rates() -> dict:
    url = f"{EXCHANGE_BASE_URL}/{EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}"
    logger.info(f"📡 Appel Exchange Rate API...")

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    raw = response.json()

    if raw.get("result") != "success":
        raise ValueError(f"API error : {raw.get('error-type')}")

    rates = {
        c: raw["conversion_rates"][c]
        for c in TARGET_CURRENCIES
        if c in raw["conversion_rates"]
    }

    for currency, rate in rates.items():
        logger.info(f"   1 {BASE_CURRENCY} = {rate:.4f} {currency}")

    return {
        "timestamp"     : datetime.utcnow().isoformat(),
        "base_currency" : BASE_CURRENCY,
        "rates"         : rates,
        "source"        : "exchangerate-api.com"
    }


def run():
    logger.info("🚀 INGESTION EXCHANGE RATES")
    gcs      = StorageClient()
    rates    = fetch_rates()
    today    = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    gcs_path = f"{GCS_RAW_EXCHANGE}/rates_{today}.json"
    gcs.upload_json(rates, gcs_path)
    logger.info(f"✅ Sauvegardé → {gcs_path}")
    return rates


if __name__ == "__main__":
    run()