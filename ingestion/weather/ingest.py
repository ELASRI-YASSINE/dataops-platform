from ingestion.base.connector import BaseConnector
from ingestion.base.uploader import GCSUploader

from config.settings import settings
from common.logger import logger

import requests
from datetime import datetime


class WeatherConnector(BaseConnector):

    def __init__(self):

        super().__init__("Weather Connector")

        self.api_key = settings.WEATHER_API_KEY

        self.uploader = GCSUploader()
