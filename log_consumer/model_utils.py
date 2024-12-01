from datetime import datetime
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
import joblib

model = joblib.load('fraud_detection_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

def predict_transaction(transaction: dict):
    df = pd.DataFrame([transaction])

    columns_to_drop = ['transaction_id', 'datetime', 'expiration_date', 'Unnamed: 0']
    test_data = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    for col, le in label_encoders.items():
        if col in test_data.columns:
            test_data[col] = le.transform(test_data[col])

    test_data_scaled = scaler.transform(test_data)

    predictions = model.predict(test_data_scaled)

    return bool(predictions)