import os
from kombu import Queue, Exchange


broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

task_queues = (
    Queue('log_consumer', Exchange('tasks'), routing_key='log_consumer.#'),
)

task_default_queue = 'log_consumer'
task_default_exchange_type = 'direct'

timezone = 'Europe/Moscow'