from ingestion.weather.ingest import WeatherConnector
from ingestion.exchange.ingest import ExchangeConnector
from ingestion.olist.ingest import OlistConnector

CONNECTORS = [
    OlistConnector,
    ExchangeConnector,
    WeatherConnector,
]
