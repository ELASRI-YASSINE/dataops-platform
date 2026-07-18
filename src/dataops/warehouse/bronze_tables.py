BRONZE_TABLES = [

    {
        "table": "bronze_orders",
        "source": "gs://dataops-pfa-datalake/processed/olist/orders/*"
    },

    {
        "table": "bronze_customers",
        "source": "gs://dataops-pfa-datalake/processed/olist/customers/*"
    },

    {
        "table": "bronze_products",
        "source": "gs://dataops-pfa-datalake/processed/olist/products/*"
    },

    {
        "table": "bronze_sellers",
        "source": "gs://dataops-pfa-datalake/processed/olist/sellers/*"
    },

    {
        "table": "bronze_payments",
        "source": "gs://dataops-pfa-datalake/processed/olist/payments/*"
    },

    {
        "table": "bronze_reviews",
        "source": "gs://dataops-pfa-datalake/processed/olist/reviews/*"
    },

    {
        "table": "bronze_geolocation",
        "source": "gs://dataops-pfa-datalake/processed/olist/geolocation/*"
    }

]
