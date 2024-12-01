from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client['bank_transactions']
collection = db['transactions']

def add_transaction(transaction, is_fraud=False):
    result = collection.insert_one({**transaction, "is_fraud": is_fraud}, bypass_document_validation=True)

def get_all_transactions(limit=20, offset=0):
    result =  list(collection.find().skip(offset).limit(limit))

    return map(lambda x: {**x, "_id": str(x["_id"])}, result)

def get_transaction_by_id(transaction_id):
    result = collection.find_one({"transaction_id": transaction_id})
    result["_id"] = str(result["_id"])

    return result   

    