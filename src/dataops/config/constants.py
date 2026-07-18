# config/constants.py
"""
Constantes globales du projet — jamais de valeurs magiques dans le code
"""

# Olist dataset files
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

# Brazilian cities for weather
BRAZILIAN_CITIES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte",
    "Brasilia",  "Curitiba",       "Porto Alegre",
    "Salvador",  "Fortaleza",      "Manaus",        "Recife"
]

# GCS paths
class GCSPaths:
    RAW_OLIST    = "raw/olist"
    RAW_EXCHANGE = "raw/api/exchange_rates"
    RAW_WEATHER  = "raw/api/weather"
    RAW_STREAM   = "raw/api/streaming"
    STAGING      = "staging/olist"
    CURATED      = "curated"

# API URLs
EXCHANGE_BASE_URL = "https://v6.exchangerate-api.com/v6"
WEATHER_BASE_URL  = "https://api.openweathermap.org/data/2.5"

# BigQuery tables
class BQTables:
    ORDERS     = "fact_orders"
    CUSTOMERS  = "dim_customers"
    PRODUCTS   = "dim_products"
    SELLERS    = "dim_sellers"
    GEOGRAPHY  = "dim_geography"
