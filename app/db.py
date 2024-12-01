import pandas as pd
from pymongo import MongoClient
from scipy.stats import pearsonr
from pandas.api.types import is_numeric_dtype

client = MongoClient("mongodb://localhost:27018/")
db = client['bank_transactions']
collection = db['transactions']

def add_all_transactions(csv_path):
    collection.insert_many(pd.read_csv(csv_path).to_dict('records'))

def add_transaction(transaction, is_fraud=False):
    collection.insert_one({**transaction, "is_fraud": is_fraud})

def get_all_transactions(limit=20, offset=0):
    result =  list(collection.find().skip(offset).limit(limit))

    return map(lambda x: {**x, "_id": str(x["_id"])}, result)

def get_transaction_by_id(transaction_id):
    result = collection.find_one({"transaction_id": transaction_id})
    result["_id"] = str(result["_id"])

    return result   

def calculate_eda():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['expiration_date'] = pd.to_datetime(df['expiration_date'])
    
    eda_metrics = {
        "total_transactions": len(df),
        "unique_clients": df['client_id'].nunique(),
        "total_fraud_cases": df[df['is_fraud'] == True].shape[0],
        "fraud_rate": df[df['is_fraud'] == True].shape[0] / len(df) if len(df) > 0 else 0,
        "average_transaction_amount": df['sum'].mean() if not df['sum'].empty else 0,
        "most_common_card_type": df['card_type'].mode()[0] if not df['card_type'].empty else None,
        "transaction_count_by_device": df['device_type'].value_counts().to_dict(),
        "fraud_by_device_type": df[df['is_fraud'] == True]['device_type'].value_counts().to_dict(),
        "transaction_volume_by_date": {
            date.isoformat(): total for date, total in df.groupby(df['datetime'].dt.date)['sum'].sum().items()
        },
    }
    
    return eda_metrics

def calculate_avg_sum_and_fraud():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])
        
    fraud_avg_sum = df[df['is_fraud'] == True]['sum'].mean()
    non_fraud_avg_sum = df[df['is_fraud'] == False]['sum'].mean()
    
    return {
        "average_sum_fraud": fraud_avg_sum,
        "average_sum_non_fraud": non_fraud_avg_sum
    }

def calculate_avg_sum_per_device():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])
        
    avg_sum_per_device = df.groupby('device_type')['sum'].mean().to_dict()
    
    avg_sum_per_device_fraud = df[df["is_fraud"] == True].groupby('device_type')['sum'].mean().to_dict()

    return {
        "average_sum_per_device": avg_sum_per_device,
        "average_sum_per_device_fraud": avg_sum_per_device_fraud
    }

def calculate_total_card_types():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    total_card_types = df['card_type'].value_counts().to_dict()
    
    return {
        "total_card_types": total_card_types
    }

def calculate_total_device_usage():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    total_device_usage = df['device_type'].value_counts().to_dict()
    
    return {
        "total_device_usage": total_device_usage
    }

def calculate_sum_distribution():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    sum_stats = {
        "mean": df['sum'].mean(),
        "median": df['sum'].median(),
        "std_dev": df['sum'].std(),
        "max": df['sum'].max(),
        "min": df['sum'].min(),
        "q1": df['sum'].quantile(0.25),
        "q3": df['sum'].quantile(0.75),
        "outliers_high": df[df['sum'] > df['sum'].mean() + 3 * df['sum'].std()]['sum'].tolist(),
        "outliers_low": df[df['sum'] < df['sum'].mean() - 3 * df['sum'].std()]['sum'].tolist()
    }
    
    return sum_stats

def calculate_fraud_percentage_per_device():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    total_fraud_transactions = len(df[df['is_fraud'] == True])
    
    if total_fraud_transactions == 0:
        return {
            "fraud_percentage_per_device": {}
        }
    
    fraud_count_per_device = df[df['is_fraud'] == True].groupby('device_type').size()
    
    normalized_fraud_percentage = (
        fraud_count_per_device
        .divide(total_fraud_transactions)
        .multiply(100)
        .to_dict()
    )
    
    return {
        "fraud_percentage_per_device": normalized_fraud_percentage
    }

def calculate_balance_distribution():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    balance_stats = {
        "mean": df['balance'].mean(),
        "median": df['balance'].median(),
        "std_dev": df['balance'].std(),
        "max": df['balance'].max(),
        "min": df['balance'].min(),
        "q1": df['balance'].quantile(0.25),
        "q3": df['balance'].quantile(0.75),
        "outliers_high": df[df['balance'] > df['balance'].mean() + 3 * df['balance'].std()]['balance'].tolist(),
        "outliers_low": df[df['balance'] < df['balance'].mean() - 3 * df['balance'].std()]['balance'].tolist()
    }
    
    return balance_stats

def calculate_fraud_percentage_per_card_type():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    fraud_percentage = (
        df[df['is_fraud'] == True]
        .groupby('card_type')
        .size()
        .divide(df.groupby('card_type').size())
        .fillna(0)
        .multiply(100)
        .to_dict()
    )
    
    return {
        "fraud_percentage_per_card_type": fraud_percentage
    }

def calculate_hourly_transaction_distribution():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    hourly_distribution = df.groupby(df['datetime'].dt.hour).size().to_dict()
    
    return {
        "hourly_transaction_distribution": hourly_distribution
    }

def calculate_transaction_sum_distribution():
    documents = list(collection.find())
    df = pd.DataFrame(documents)

    if df.empty:
        return {"labels": [], "values": []}
    
    bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]  # Add +1 to include the max value
    labels = ["0-100", "101-200", "201-300", "301-400", "401-500", "501-600", "601-700", "701-800", "801-900", "901-1000", "1001-1100", "1101-1200", "1201-1300", "1301-1400", "1401-1500"]
    
    df['sum_bin'] = pd.cut(df['sum'], bins=bins, labels=labels, right=False)
    
    sum_distribution = df['sum_bin'].value_counts().sort_index().to_dict()
    
    return {
        "labels": list(sum_distribution.keys()),
        "values": list(sum_distribution.values())
    }

def calculate_transaction_sum_distribution_fraud():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    df = df[df['is_fraud'] == True]
    
    if df.empty:
        return {"labels": [], "values": []}
    
    max_sum = df['sum'].max()
    bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]  # Add +1 to include the max value
    labels = ["0-100", "101-200", "201-300", "301-400", "401-500", "501-600", "601-700", "701-800", "801-900", "901-1000", "1001-1100", "1101-1200", "1201-1300", "1301-1400", "1401-1500"]
    
    df['sum_bin'] = pd.cut(df['sum'], bins=bins, labels=labels, right=False)
    
    sum_distribution = df['sum_bin'].value_counts().sort_index().to_dict()
    
    return {
        "labels": list(sum_distribution.keys()),
        "values": list(sum_distribution.values())
    }

def calculate_fraud_vs_normal_by_mcc():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if df.empty:
        return {"labels": [], "fraud_values": [], "normal_values": []}
    
    fraud_count = df[df['is_fraud'] == True]['mcc'].value_counts()
    normal_count = df[df['is_fraud'] == False]['mcc'].value_counts()

    top_fraud_mccs = fraud_count.nlargest(10).index.tolist()
    
    labels = top_fraud_mccs
    fraud_values = [fraud_count.get(label, 0) for label in labels]
    normal_values = [normal_count.get(label, 0) for label in labels]
    
    return {
        "labels": labels,
        "fraud_values": list(map(lambda x: int(x), fraud_values)),
        "normal_values": list(map(lambda x: int(x), normal_values))
    }

def calculate_fraud_vs_normal_by_device_id():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if df.empty:
        return {"labels": [], "fraud_values": [], "normal_values": []}

    fraud_count = df[df['is_fraud'] == True]['device_id'].value_counts()
    normal_count = df[df['is_fraud'] == False]['device_id'].value_counts()

    top_fraud_device_id = fraud_count.nlargest(10).index.tolist()
    
    labels = top_fraud_device_id
    fraud_values = [fraud_count.get(label, 0) for label in labels]
    normal_values = [normal_count.get(label, 0) for label in labels]
    
    return {
        "labels": labels,
        "fraud_values": list(map(lambda x: int(x), fraud_values)),
        "normal_values": list(map(lambda x: int(x), normal_values))
    }

def calculate_fraud_vs_normal_by_operation_type():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if df.empty:
        return {"labels": [], "fraud_values": [], "normal_values": []}

    fraud_count = df[df['is_fraud'] == True]['oper_type'].value_counts()
    normal_count = df[df['is_fraud'] == False]['oper_type'].value_counts()

    top_fraud_oper_types = fraud_count.nlargest(10).index.tolist()
    
    labels = top_fraud_oper_types
    fraud_values = [fraud_count.get(label, 0) for label in labels]
    normal_values = [normal_count.get(label, 0) for label in labels]
    
    return {
        "labels": labels,
        "fraud_values": list(map(lambda x: int(x), fraud_values)),
        "normal_values": list(map(lambda x: int(x), normal_values))
    }

def calculate_fraud_by_pin_incorrect_count():
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    
    if df.empty:
        return {"labels": [], "fraud_values": []}

    fraud_count = df[df['is_fraud'] == True].groupby('pin_inc_count').size()
    normal_count = df[df['is_fraud'] == False].groupby('pin_inc_count').size()
    
    top_fraud_pin_counts = fraud_count.nlargest(10).index.tolist()
    
    labels = sorted(top_fraud_pin_counts)  # Sort for consistent charting
    fraud_values = [fraud_count.get(label, 0) for label in labels]
    normal_values = [normal_count.get(label, 0) for label in labels]
    
    return {
        "labels": labels,
        "values": list(map(lambda x: int(x), fraud_values)),
        "normal_values": list(map(lambda x: int(x), normal_values))
    }
