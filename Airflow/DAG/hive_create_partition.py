#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import airflow

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators import BashOperator, DummyOperator

from datetime import datetime, timedelta


# --------------------------------------------------------------------------------
# set default arguments
# --------------------------------------------------------------------------------

default_args = {
    'owner': 'Jaimin',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'hive_create_part_v1',
    default_args=default_args,
    schedule_interval="0 1 * * *",
    concurrency=1)

# --------------------------------------------------------------------------------
# set tasks 
# --------------------------------------------------------------------------------

task = BashOperator(
    task_id='hive_create_parition',
    bash_command='bash /data/appdata/airflow/script/hive_create_job.sh mnode2 ',
    dag=dag)
