from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'test_connection_dag',
    default_args=default_args,
    description='A DAG to test retrieving a connection',
    schedule='@weekly',  # Equivalent to weekly schedule
    start_date=datetime(2025, 3, 1),
    catchup=False,
    tags=['test', 'connection'],
)

def get_connection():
    try:
        conn = BaseHook.get_connection(conn_id="test_id")
        print(f"Connection retrieved successfully: {conn.conn_id}")
        print(f"Host: {conn.host}")
        print(f"Schema: {conn.schema}")
        print(f"Login: {conn.login}")
        print(f"Port: {conn.port}")
        print(f"URI: {conn.get_uri()}")
        return "Connection retrieved successfully!"
    except Exception as e:
        print(f"Error retrieving connection: {e}")
        return f"Error: {e}"

test_connection_task = PythonOperator(
    task_id='test_connection',
    python_callable=get_connection,
    dag=dag,
)

# Set task dependencies
test_connection_task