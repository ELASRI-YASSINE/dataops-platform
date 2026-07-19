# src/dataops/orchestration/dags/dataops_pipeline.py
"""
DAG Master — orchestre tout le pipeline DataOps
Déclenche ingestion_pipeline puis transformation_pipeline
Fréquence : Tous les jours à 4h du matin
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago

default_args = {
    "owner"            : "dataops",
    "retries"          : 1,
    "retry_delay"      : timedelta(minutes=5),
    "email_on_failure" : False,
}

dag = DAG(
    dag_id="dataops_master",
    description="DAG Master — déclenche ingestion puis transformation",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["dataops", "master"],
)

start = EmptyOperator(task_id="start", dag=dag)
end   = EmptyOperator(task_id="end",   dag=dag)

# ── Step 1 : Déclenche l'ingestion ────────────────────────────────────────
trigger_ingestion = TriggerDagRunOperator(
    task_id="trigger_ingestion",
    trigger_dag_id="ingestion_pipeline",
    wait_for_completion=True,
    dag=dag,
)

# ── Step 2 : Attend que l'ingestion soit terminée ─────────────────────────
wait_ingestion = ExternalTaskSensor(
    task_id="wait_ingestion_complete",
    external_dag_id="ingestion_pipeline",
    external_task_id="end",
    timeout=3600,
    mode="poke",
    poke_interval=60,
    dag=dag,
)

# ── Step 3 : Déclenche la transformation ──────────────────────────────────
trigger_transformation = TriggerDagRunOperator(
    task_id="trigger_transformation",
    trigger_dag_id="transformation_pipeline",
    wait_for_completion=True,
    dag=dag,
)

# ── Dependencies ───────────────────────────────────────────────────────────
start >> trigger_ingestion >> wait_ingestion >> trigger_transformation >> end
