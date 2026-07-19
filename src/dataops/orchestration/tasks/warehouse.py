from airflow.operators.bash import BashOperator


def create_warehouse_task(dag):

    return BashOperator(

        task_id="bigquery_bronze",

        bash_command="""
        cd /opt/airflow/project

        export PYTHONPATH=/opt/airflow/project/src

        python src/dataops/warehouse/pipeline.py
        """,

        dag=dag

    )
