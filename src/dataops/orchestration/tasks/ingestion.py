from airflow.operators.bash import BashOperator


def create_ingestion_task(dag):

    return BashOperator(

        task_id="ingestion",

        bash_command="""
        cd /opt/airflow/project

        export PYTHONPATH=/opt/airflow/project/src

        python src/dataops/pipeline.py
        """,

        dag=dag

    )
