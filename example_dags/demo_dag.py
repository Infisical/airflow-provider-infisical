from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

from airflow.models.variable import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

dag = DAG(
    'simple_demo_dag',
    default_args=default_args,
    description='A simple demo DAG',
    schedule='@weekly',  # Equivalent to weekly schedule
    start_date=datetime(2025, 3, 18),
    catchup=False,
    tags=['demo'],
)

def print_variable():
  my_var = Variable.get('TEST_VARIABLE') 
  logging.info(f'var_name value: {my_var}')

task2 = PythonOperator(
    task_id='print_variable_test_variable',
    python_callable=print_variable,
    dag=dag,
)

# Set task dependencies
task2