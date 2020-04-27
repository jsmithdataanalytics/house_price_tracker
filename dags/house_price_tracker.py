from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import timezone

from tasks import get_listings, send_email

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'james',
    'depends_on_past': True,
    'wait_for_downstream': True,
    'start_date': timezone.datetime(year=2020, month=1, day=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'house_price_tracker',
    default_args=default_args,
    catchup=False,
    description='Retrieves Zoopla property listings and analyses prices',
    schedule_interval=timedelta(days=1)
)

t1 = PythonOperator(
    task_id='get_listings',
    python_callable=get_listings,
    dag=dag,
)

t2 = PythonOperator(
    task_id='send_email',
    provide_context=True,
    python_callable=send_email,
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
