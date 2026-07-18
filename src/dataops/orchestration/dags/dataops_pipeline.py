from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "yassine",
    "retries": 2,
}

with DAG(
    dag_id="dataops_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    start = BashOperator(
        task_id="start_pipeline",
        bash_command="echo 'Pipeline Started'"
    )

    finish = BashOperator(
        task_id="finish_pipeline",
        bash_command="echo 'Pipeline Finished'"
    )

    start >> finish
