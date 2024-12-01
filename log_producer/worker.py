from app import celery_app
import pandas as pd

import time
import random

def send_log(log):
    celery_app.send_task('log_consumer.consume_log', kwargs={
        'log': log
    }, queue='log_consumer')

def read_and_send_log(file_path):
    print(f'Reading {file_path}')
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        send_log(row.to_dict())

        time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    read_and_send_log('dataset.csv')