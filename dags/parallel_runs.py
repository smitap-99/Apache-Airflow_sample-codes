from asyncio import Task, tasks
from multiprocessing import process
from urllib import response
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
# from airflow.operators.subdag import SubDagOperator

from datetime import datetime
# from subdags.subdag_parallel_processing import subdag_parallel_processing

default_args = {
        'start_date' : datetime(2020, 1, 1)
        }

with DAG('parallel_runs', schedule_interval='@daily',
        default_args = default_args,
        catchup=False) as dag:

    task_1=BashOperator(
            task_id='task_1',
            bash_command='sleep 3'
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        task_2=BashOperator(
            task_id='task_2',
            bash_command='sleep 3'
        )

        # task_3=BashOperator(
        #         task_id='task_3',
        #         bash_command='sleep 3'
        # )
        with TaskGroup('spark_tasks') as spark_tasks:
                task_3=BashOperator(
                task_id='task_3',
                bash_command='sleep 3'
                )

        with TaskGroup('flink_tasks') as flink_tasks:
                task_3=BashOperator(
                task_id='task_3',
                bash_command='sleep 3'
                )

#     processing = SubDagOperator(
#             task_id='processing_tasks',
#             subdag=subdag_parallel_processing('parallel_runs', 'processing_tasks', default_args)
#     )

    task_4=BashOperator(
            task_id='task_4',
            bash_command='sleep 3'
    )

    task_1 >> processing_tasks >> task_4 


