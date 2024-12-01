from celery import Celery

celery_app = Celery(
    'log_consumer',
    include=['tasks']
)

celery_app.config_from_object('config')
celery_app.autodiscover_tasks()