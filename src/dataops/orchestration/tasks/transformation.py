from airflow.operators.bash import BashOperator


def create_transformation_task(dag):

    return BashOperator(

        task_id="spark_processing",

        bash_command="""
        cd /opt/airflow/project

        gcloud dataproc batches submit pyspark \
        src/dataops/transformation/jobs/process_dataset.py \
        --region=europe-west1 \
        --deps-bucket=gs://dataops-pfa-temp \
        --py-files=src/dataops.zip
        """,

        dag=dag

    )
