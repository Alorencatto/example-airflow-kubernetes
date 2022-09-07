from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

with DAG(dag_id="catchup_example.py",
                schedule_interval= "@daily",
                catchup=False,
                start_date = days_ago(3),
                max_active_runs=1) as dag:
    
    task_1 = DummyOperator(
        task_id = "task_1"
    )