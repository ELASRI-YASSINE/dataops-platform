# src/dataops/orchestration/dags/ingestion_dag.py
"""
DAG d'ingestion des données
Orchestre : Olist + Exchange Rates + Weather → GCS
Fréquence : Tous les jours à 5h du matin
"""

import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

sys.path.insert(0, "/opt/airflow/dags/src")

default_args = {
    "owner"            : "dataops",
    "retries"          : 2,
    "retry_delay"      : timedelta(minutes=3),
    "email_on_failure" : False,
}

dag = DAG(
    dag_id="ingestion_pipeline",
    description="Ingestion Olist + Exchange + Weather vers GCS",
    default_args=default_args,
    schedule_interval="0 5 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["dataops", "ingestion"],
)

# ── Start ──────────────────────────────────────────────────────────────────
start = EmptyOperator(task_id="start", dag=dag)
end   = EmptyOperator(task_id="end",   dag=dag)

# ── Task 1 : Olist ─────────────────────────────────────────────────────────
def run_olist_ingestion(**context):
    """
    Ingestion du dataset Olist
    Upload les 8 CSV depuis GCS raw/olist/
    """
    from dataops.ingestion.olist.ingest import OlistConnector
    connector = OlistConnector(data_folder="/opt/airflow/dags/data/")
    success   = connector.run()

    if not success:
        raise Exception("❌ Olist ingestion échouée")

    # XCom : partage le résultat avec les tasks suivantes
    context["ti"].xcom_push(key="olist_status", value="success")
    print("✅ Olist ingestion terminée")


task_olist = PythonOperator(
    task_id="ingest_olist",
    python_callable=run_olist_ingestion,
    dag=dag,
    provide_context=True,
)

# ── Task 2 : Exchange Rates ────────────────────────────────────────────────
def run_exchange_ingestion(**context):
    """
    Ingestion des taux de change BRL → USD/EUR/MAD
    Appelle l'API exchangerate-api.com
    """
    from dataops.ingestion.exchange.ingest import ExchangeConnector
    connector = ExchangeConnector()
    success   = connector.run()

    if not success:
        raise Exception("❌ Exchange Rate ingestion échouée")

    context["ti"].xcom_push(key="exchange_status", value="success")
    print("✅ Exchange Rate ingestion terminée")


task_exchange = PythonOperator(
    task_id="ingest_exchange_rates",
    python_callable=run_exchange_ingestion,
    dag=dag,
    provide_context=True,
)

# ── Task 3 : Weather ───────────────────────────────────────────────────────
def run_weather_ingestion(**context):
    """
    Ingestion météo des 10 villes brésiliennes
    Appelle l'API OpenWeatherMap
    """
    from dataops.ingestion.weather.ingest import WeatherConnector
    connector = WeatherConnector()
    success   = connector.run()

    if not success:
        raise Exception("❌ Weather ingestion échouée")

    context["ti"].xcom_push(key="weather_status", value="success")
    print("✅ Weather ingestion terminée")


task_weather = PythonOperator(
    task_id="ingest_weather",
    python_callable=run_weather_ingestion,
    dag=dag,
    provide_context=True,
)

# ── Task 4 : Rapport ───────────────────────────────────────────────────────
def ingestion_report(**context):
    """
    Génère un rapport de l'ingestion
    Lit les XCom des tasks précédentes
    """
    ti = context["ti"]
    olist_status    = ti.xcom_pull(task_ids="ingest_olist",          key="olist_status")
    exchange_status = ti.xcom_pull(task_ids="ingest_exchange_rates",  key="exchange_status")
    weather_status  = ti.xcom_pull(task_ids="ingest_weather",         key="weather_status")

    print("=" * 50)
    print("📊 RAPPORT INGESTION")
    print("=" * 50)
    print(f"  Olist          : {olist_status}")
    print(f"  Exchange Rates : {exchange_status}")
    print(f"  Weather        : {weather_status}")
    print(f"  Date           : {context['ds']}")
    print("=" * 50)


task_report = PythonOperator(
    task_id="ingestion_report",
    python_callable=ingestion_report,
    dag=dag,
    provide_context=True,
    trigger_rule="all_done",   # S'exécute même si une task échoue
)

# ── Dependencies ───────────────────────────────────────────────────────────
start >> [task_olist, task_exchange, task_weather] >> task_report >> end
