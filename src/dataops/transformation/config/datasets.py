DATASETS = [
    {
        "name": "orders",
        "input": "gs://dataops-pfa-datalake/raw/olist/orders/olist_orders_dataset.csv",
        "output": "gs://dataops-pfa-datalake/processed/olist/orders/"
    },
    {
        "name": "customers",
        "input": "gs://dataops-pfa-datalake/raw/olist/customers/olist_customers_dataset.csv",
        "output": "gs://dataops-pfa-datalake/processed/olist/customers/"
    },
    {
        "name": "products",
        "input": "gs://dataops-pfa-datalake/raw/olist/products/olist_products_dataset.csv",
        "output": "gs://dataops-pfa-datalake/processed/olist/products/"
    },
    {
        "name": "payments",
        "input": "gs://dataops-pfa-datalake/raw/olist/payments/olist_order_payments_dataset.csv",
        "output": "gs://dataops-pfa-datalake/processed/olist/payments/"
    },
    {
        "name": "reviews",
        "input": "gs://dataops-pfa-datalake/raw/olist/reviews/olist_order_reviews_dataset.csv",
        "output": "gs://dataops-pfa-datalake/processed/olist/reviews/"
    }
]
