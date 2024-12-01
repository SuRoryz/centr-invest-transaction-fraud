from celery import Celery

celery_app = Celery(
    'log_producer'
)

celery_app.config_from_object('config')