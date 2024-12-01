from fastapi import APIRouter
from fastapi.responses import JSONResponse
from openai import BaseModel
from model_utils import predict_transaction
from db import *
from utils.ip_address_finder import print_ip_info

router = APIRouter()

class Transaction(BaseModel):
    transaction_id: str
    ip: str
    device_id: str
    device_type: str
    tran_code: str
    mcc: str
    client_id: str
    card_type: str
    pin_inc_count: int
    card_status: str
    expiration_date: str
    datetime: str
    sum: float
    oper_type: str
    balance: float
    
@router.post("/predict")
async def predict(transaction: Transaction):
    transaction = transaction.dict()

    result = predict_transaction(transaction)
    add_transaction(transaction, is_fraud=result)

    return result

@router.post("/add_all_transactions")
async def predict(transaction: Transaction):
    add_all_transactions('dataset.csv')

@router.get("/transactions")
async def get_transactions():
    return list(get_all_transactions())

@router.get("/get_ip_data")
async def get_transactions(ip: str):
    return print_ip_info(ip)

@router.get("/eda")
async def get_eda():
    eda_data = calculate_eda()

    return JSONResponse(content=eda_data)

@router.get("/analytics/avg_sum_and_fraud")
async def get_avg_sum_and_fraud():
    data = calculate_avg_sum_and_fraud()
    return JSONResponse(content=data)

@router.get("/analytics/avg_sum_per_device")
async def get_avg_sum_per_device():
    data = calculate_avg_sum_per_device()
    return JSONResponse(content=data)

@router.get("/analytics/total_card_types")
async def get_total_card_types():
    data = calculate_total_card_types()
    return JSONResponse(content=data)

@router.get("/analytics/total_device_usage")
async def get_total_device_usage():
    data = calculate_total_device_usage()
    return JSONResponse(content=data)

@router.get("/analytics/sum_distribution")
async def get_sum_distribution():
    data = calculate_transaction_sum_distribution()
    return JSONResponse(content=data)

@router.get("/analytics/sum_distribution_fraud")
async def get_sum_distribution():
    data = calculate_transaction_sum_distribution_fraud()
    return JSONResponse(content=data)

@router.get("/analytics/fraud_percentage_per_device")
async def get_fraud_percentage_per_device():
    data = calculate_fraud_percentage_per_device()
    return JSONResponse(content=data)

@router.get("/analytics/fraud_percentage_per_card_type")
async def get_fraud_percentage_per_card_type():
    data = calculate_fraud_percentage_per_card_type()
    return JSONResponse(content=data)

@router.get("/analytics/hourly_transaction_distribution")
async def get_hourly_transaction_distribution():
    data = calculate_hourly_transaction_distribution()
    return JSONResponse(content=data)

@router.get("/analytics/total_transaction_by_mcc")
async def get_total_transaction_by_mcc():
    data = calculate_fraud_vs_normal_by_mcc()
    return JSONResponse(content=data)

@router.get("/analytics/total_transaction_by_device_id")
async def get_total_transaction_by_mcc():
    data = calculate_fraud_vs_normal_by_device_id()
    return JSONResponse(content=data)

@router.get("/analytics/total_transaction_by_type")
async def get_total_transaction_by_type():
    data = calculate_fraud_vs_normal_by_operation_type()
    return JSONResponse(content=data)

@router.get("/analytics/total_transaction_by_pin")
async def get_total_transaction_by_pin():
    data = calculate_fraud_by_pin_incorrect_count()
    return JSONResponse(content=data)