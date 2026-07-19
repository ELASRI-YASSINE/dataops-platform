from airflow.operators.bash import BashOperator


def create_dbt_task(dag):

    return BashOperator(

        task_id="dbt",

        bash_command="""
        cd /opt/airflow/project/dbt/dataops_dbt

        dbt run
        """,

        dag=dag

    )
