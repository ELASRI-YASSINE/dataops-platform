# ingestion/exchange/ingest.py
import requests
from datetime import datetime
from ingestion.base.connector import BaseConnector
from ingestion.base.uploader import GCSUploader
from config.constants import (
    EXCHANGE_BASE_URL, BASE_CURRENCY,
    TARGET_CURRENCIES, GCSPaths
)
from config.settings import settings
from common.exceptions import APIError
from common.utils import get_timestamp

class ExchangeConnector(BaseConnector):
    """Connecteur pour l'API Exchange Rate"""

    def __init__(self):
        super().__init__()
        self.uploader = GCSUploader()

    def extract(self) -> dict:
        url = f"{EXCHANGE_BASE_URL}/{settings.EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}"
        self.logger.info(f"📡 Appel Exchange Rate API — base: {BASE_CURRENCY}")

        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            raise APIError("ExchangeRate", response.status_code, response.text)

        raw = response.json()
        if raw.get("result") != "success":
            raise APIError("ExchangeRate", 0, raw.get("error-type", "unknown"))

        rates = {
            c: raw["conversion_rates"][c]
            for c in TARGET_CURRENCIES
            if c in raw["conversion_rates"]
        }

        for currency, rate in rates.items():
            self.logger.info(f"   1 {BASE_CURRENCY} = {rate:.4f} {currency}")

        return {
            "timestamp"     : datetime.utcnow().isoformat(),
            "base_currency" : BASE_CURRENCY,
            "rates"         : rates,
            "source"        : "exchangerate-api.com"
        }

    def validate(self, data: dict) -> bool:
        if not data.get("rates"):
            self.logger.error("❌ Aucun taux de change reçu")
            return False
        if len(data["rates"]) < 3:
            self.logger.warning("⚠️  Peu de devises reçues")
        return True

    def load(self, data: dict) -> bool:
        gcs_path = f"{GCSPaths.RAW_EXCHANGE}/rates_{get_timestamp()}.json"
        return self.uploader.upload_json(data, gcs_path)
