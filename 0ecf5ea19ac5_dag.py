from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator, DatabricksRunNowOperator
from datetime import datetime, timedelta 


#Define params for Submit Run Operator
notebook_task = {
    'notebook_path': '/Users/shahara.khaleque@gmail.com/databricks_batch_processing.ipynb',
}


#Define params for Run Now Operator
notebook_params = {
    "Variable":5
}


default_args = {
    'owner': 'setokeza',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': '2',
    'retry_delay': timedelta(minutes=2)
}


with DAG('0ecf5ea19ac5_dag',
    # should be a datetime format
    start_date=datetime(2023, 12, 31),
    # run daily at midnight
    schedule_interval='* 0 * * * *',
    catchup=False,
    default_args=default_args
    ) as dag:


    opr_submit_run = DatabricksSubmitRunOperator(
        task_id='submit_run',
        # the connection we set-up previously
        databricks_conn_id='databricks_default',
        existing_cluster_id='1108-162752-8okw8dgg',
        notebook_task=notebook_task
    )
    opr_submit_run