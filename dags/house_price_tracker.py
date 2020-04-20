from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'james',
    'depends_on_past': True,
    'wait_for_downstream': True,
    'start_date': datetime(year=2020, month=1, day=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'house_price_tracker',
    default_args=default_args,
    catchup=False,
    description='Retrieves Zoopla property listings and analyses prices',
    schedule_interval=timedelta(days=7),
)

t1 = PythonOperator(
    task_id='get_listings',
    python_callable=print,
    op_args=['Task 1 Success!'],
    dag=dag,
)

t2 = PythonOperator(
    task_id='send_email',
    python_callable=print,
    op_args=['Task 2 Success!'],
    dag=dag,
)

# noinspection PyStatementEffect
t1 >> t2

# Documentation
dag.doc_md = f"""
#### DAG Documentation
{dag.description}
"""

t1.doc_md = """
#### Task Documentation
Retrieves and stores Zoopla data
"""

t2.doc_md = """
#### Task Documentation
Sends email notification when new data is available
"""
