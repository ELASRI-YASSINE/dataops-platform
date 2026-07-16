import os
from dotenv import load_dotenv

load_dotenv()

# GCP
PROJECT_ID  = os.getenv("GCP_PROJECT_ID",  "dataops-pfa-502611")
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME", "dataops-pfa-datalake")
REGION      = os.getenv("GCP_REGION",      "europe-west1")

# APIs
EXCHANGE_API_KEY  = os.getenv("EXCHANGE_RATE_API_KEY")
WEATHER_API_KEY   = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_BASE_URL = "https://v6.exchangerate-api.com/v6"
WEATHER_BASE_URL  = "https://api.openweathermap.org/data/2.5"

# Olist files
OLIST_FILES = {
    "olist_orders_dataset.csv"         : "orders",
    "olist_order_items_dataset.csv"    : "order_items",
    "olist_customers_dataset.csv"      : "customers",
    "olist_products_dataset.csv"       : "products",
    "olist_sellers_dataset.csv"        : "sellers",
    "olist_order_payments_dataset.csv" : "payments",
    "olist_order_reviews_dataset.csv"  : "reviews",
    "olist_geolocation_dataset.csv"    : "geolocation",
}

# Currencies
BASE_CURRENCY     = "BRL"
TARGET_CURRENCIES = ["USD", "EUR", "MAD", "GBP", "ARS", "MXN"]

# Cities
BRAZILIAN_CITIES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte",
    "Brasilia",  "Curitiba",       "Porto Alegre",
    "Salvador",  "Fortaleza",      "Manaus", "Recife"
]

# GCS paths
GCS_RAW_OLIST    = "raw/olist"
GCS_RAW_EXCHANGE = "raw/api/exchange_rates"
GCS_RAW_WEATHER  = "raw/api/weather"
GCS_STAGING      = "staging/olist"
GCS_CURATED      = "curated"