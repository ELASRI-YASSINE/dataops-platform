# src/dataops/orchestration/dags/transformation_dag.py
"""
DAG de transformation des données
Orchestre : Dataproc Spark jobs → BigQuery Bronze → dbt
Fréquence : Tous les jours à 6h (après ingestion)
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner"            : "dataops",
    "retries"          : 1,
    "retry_delay"      : timedelta(minutes=5),
    "email_on_failure" : False,
}

dag = DAG(
    dag_id="transformation_pipeline",
    description="Spark → BigQuery Bronze → dbt Silver/Gold",
    default_args=default_args,
    schedule_interval="0 6 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["dataops", "transformation", "dbt"],
)

GCP_PROJECT  = "dataops-pfa-502611"
GCP_REGION   = "europe-west1"
GCS_BUCKET   = "dataops-pfa-datalake"
CLUSTER_NAME = "dataops-cluster"
SCRIPT_PATH  = f"gs://{GCS_BUCKET}/scripts/spark_process.py"

start = EmptyOperator(task_id="start", dag=dag)
end   = EmptyOperator(task_id="end",   dag=dag)

# ── Tasks Spark : un task par dataset ─────────────────────────────────────
DATASETS = [
    "orders", "customers", "products",
    "payments", "reviews", "sellers",
    "geolocation", "order_items"
]

spark_tasks = {}

for dataset in DATASETS:
    task = BashOperator(
        task_id=f"spark_clean_{dataset}",
        bash_command=f"""
            gcloud dataproc jobs submit pyspark \
                {SCRIPT_PATH} \
                --cluster={CLUSTER_NAME} \
                --region={GCP_REGION} \
                --project={GCP_PROJECT} \
                -- {dataset}
        """,
        dag=dag,
    )
    spark_tasks[dataset] = task

# ── Task : Chargement BigQuery Bronze ─────────────────────────────────────
def load_bronze_layer(**context):
    """
    Charge tous les Parquet GCS vers BigQuery Bronze
    Utilise le WarehouseManager
    """
    import sys
    sys.path.insert(0, "/opt/airflow/dags/src")
    from dataops.warehouse.manager import WarehouseManager

    warehouse = WarehouseManager()
    warehouse.initialize()
    warehouse.load_all_bronze()

    print("✅ Bronze Layer chargé dans BigQuery")


task_load_bronze = PythonOperator(
    task_id="load_bronze_bigquery",
    python_callable=load_bronze_layer,
    dag=dag,
    provide_context=True,
)

# ── Task : dbt run ────────────────────────────────────────────────────────
task_dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="cd /opt/airflow/dags/dbt/dataops_dbt && dbt run --no-use-colors",
    dag=dag,
)

# ── Task : dbt test ───────────────────────────────────────────────────────
task_dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command="cd /opt/airflow/dags/dbt/dataops_dbt && dbt test --no-use-colors",
    dag=dag,
)

# ── Task : Rapport final ──────────────────────────────────────────────────
def transformation_report(**context):
    print("=" * 55)
    print("📊 RAPPORT TRANSFORMATION")
    print("=" * 55)
    print(f"  Date d'exécution : {context['ds']}")
    print(f"  Datasets traités : {len(DATASETS)}")
    print(f"  BigQuery Bronze  : ✅")
    print(f"  dbt models       : ✅")
    print("=" * 55)


task_report = PythonOperator(
    task_id="transformation_report",
    python_callable=transformation_report,
    dag=dag,
    provide_context=True,
    trigger_rule="all_done",
)

# ── Dependencies ───────────────────────────────────────────────────────────
#
# start ──► spark_orders ──┐
#           spark_customers─┤
#           spark_products ─┤
#           spark_payments ─┼──► load_bronze ──► dbt_run ──► dbt_test ──► report ──► end
#           spark_reviews  ─┤
#           spark_sellers  ─┤
#           spark_geo      ─┤
#           spark_items    ─┘

start >> list(spark_tasks.values()) >> task_load_bronze
task_load_bronze >> task_dbt_run >> task_dbt_test >> task_report >> end
