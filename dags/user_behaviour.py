from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Config
def download_csv_s3_func(key:str, bucket_name:str, local_path:str):
    hook = S3Hook(aws_conn_id='aws_default')
    hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2024, 10, 11),  # Consider changing this to a past date
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,  
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "user_behaviour",
    default_args=default_args,
    schedule_interval="0 0 * * *",  # This runs the DAG daily at midnight
    max_active_runs=1,
)

# extract_user_purchase_data = PostgresOperator(
#     dag=dag,
#     task_id="extract_user_purchase_data",
#     sql="./sql/unload_user_purchase.sql",
#     postgres_conn_id="postgres_default",
#     params={"user_purchase": "/temp/user_purchase.csv"}
# )

# Task to run `dbt snapshot`
dbt_snapshot = BashOperator(
    task_id='dbt_snapshot',
    bash_command='dbt snapshot --project-dir /opt/airflow/dbt/data_pipeline/ --profiles-dir /opt/airflow/dbt/data_pipeline/profiles/',  # Update paths
    dag=dag,
    retries=1,
)

# Task to run `dbt run`
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --project-dir /opt/airflow/dbt/data_pipeline/ --profiles-dir /opt/airflow/dbt/data_pipeline/profiles/',  # Update paths
    dag=dag,
    retries=1,
)

# Task to run `dbt test` (optional)
# dbt_test = BashOperator(
#     task_id='dbt_test',
#     bash_command='dbt test --project-dir /opt/airflow/dbt/data_pipeline --profiles-dir /opt/airflow/dbt/data_pipeline/profiles/',  # Update paths
#     dag=dag,
#     retries=1,
# )

# #Task: Download CSV from S3 to Local
# download_csv_s3 = PythonOperator(
#     task_id='download_csv_s3',
#     dag=dag,
#     python_callable=download_csv_s3_func,
#     op_kwargs={
#         'key':'OnlineRetail.csv',
#         'bucket_name':'tgou1055-utilities',
#         'local_path':'/opt/airflow/data/'
#     },
#     depends_on_past=True,
#     wait_for_downstream=True,
# )

# Add S3 file check mechanism before loading data
# Step new: Task to load data from S3 to Snowflake raw table
load_raw_data_to_snowflake = SnowflakeOperator(
    dag=dag,
    task_id='load_s3_to_snowflake',
    snowflake_conn_id='snowflake_conn',
    sql=""" 
        COPY INTO DBT_DB.DBT_SCHEMA_RAW_LAYER.customers 
        FROM '@DBT_DB.DBT_SCHEMA_RAW_LAYER.staging_csv_files/customers/'
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

        COPY INTO DBT_DB.DBT_SCHEMA_RAW_LAYER.orders
        FROM '@DBT_DB.DBT_SCHEMA_RAW_LAYER.staging_csv_files/orders/'
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);

        COPY INTO DBT_DB.DBT_SCHEMA_RAW_LAYER.state
        FROM '@DBT_DB.DBT_SCHEMA_RAW_LAYER.staging_csv_files/state/'
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);
        """,
    warehouse='dbt_wh',
    database='dbt_db',
    schema='dbt_schema_raw_layer',
    role='dbt_role'
)

end_of_data_pipeline = DummyOperator(task_id="end_of_data_pipeline",dag=dag)

# pipeline
# download_csv_s3 >> 

#extract_user_purchase_data >> dbt_test >> dbt_run >> end_of_data_pipeline

# load_to_snowflake >> end_of_data_pipeline

load_raw_data_to_snowflake >> dbt_snapshot >> dbt_run >> end_of_data_pipeline 