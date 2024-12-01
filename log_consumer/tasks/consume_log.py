import asyncio
from app import celery_app
from model_utils import predict_transaction
from db import add_transaction

from socket_manager import sio

@celery_app.task(name="log_consumer.consume_log")
def consume_log(log: dict):
    result = predict_transaction(log)
    add_transaction(log, is_fraud=result)

    sio.emit("log", {**log, "is_fraud": result}, room="listen_log")
