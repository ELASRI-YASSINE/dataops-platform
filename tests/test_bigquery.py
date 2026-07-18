from dataops.warehouse.manager import WarehouseManager


warehouse = WarehouseManager()

warehouse.initialize()

warehouse.load(

    source_uri="gs://dataops-pfa-datalake/processed/olist/orders/*",

    table="bronze_orders"

)
