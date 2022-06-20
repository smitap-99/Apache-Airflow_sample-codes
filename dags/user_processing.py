from asyncio import Task, tasks
from multiprocessing import process
from urllib import response
from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from pandas import json_normalize
import json

default_args = {
        'start_date' : datetime(2020, 1, 1)
        }

def _processing_users(ti):
        users = ti.xcom_pull(task_ids=['extract_users'])
        if not len(users) or 'results' not in users[0]:
            raise ValueError('User is empty')
        user = users[0]['results'][0]
        processed_user=json_normalize({
            'firstname': user['name']['first'],
            'lastname': user['name']['last'],
            'country': user['location']['country'],
            'username': user['login']['username'],
            'password': user['login']['password'],
            'email': user['email']
        })
        processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

with DAG('user_processing', schedule_interval='@daily',
        default_args = default_args,
        catchup=False) as dag:

    creating_table = SqliteOperator(
            task_id='creating_table',
            sqlite_conn_id='db_sqlite',
            sql='''
                CREATE TABLE IF NOT EXISTS users (
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    country TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL
                );
                '''
            )
    
    is_api_available=HttpSensor(
            task_id='is_api_available',
            http_conn_id='user_api',
            endpoint='api/'
        )

    extract_users=SimpleHttpOperator(
            task_id='extract_users',
            http_conn_id='user_api',
            endpoint='api/',
            method='GET',
            response_filter=lambda response: json.loads(response.text),
            log_response=True
    )

    processing_users=PythonOperator(
            task_id='processing_users',
            python_callable=_processing_users
    )

    storing_user=BashOperator(
            task_id='storing_user',
            bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /home/smita/airflow/airflow.db'
    )

    creating_table >> is_api_available >> extract_users >> processing_users >> storing_user 


