from datetime import datetime
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
import joblib

model = joblib.load('fraud_detection_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Define a function to handle unseen labels
def safe_label_encode(series, encoder):
    unique_labels = encoder.classes_

    mapping = {label: idx for idx, label in enumerate(unique_labels)}
    encoded = series.map(lambda x: mapping.get(x, -1))
    return encoded.fillna(-1).astype(int)

def predict_transaction(transaction: dict):
    df = pd.DataFrame([transaction])

    columns_to_drop = ['transaction_id', 'datetime', 'expiration_date']
    test_data = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    for col, le in label_encoders.items():
        if col in test_data.columns:
            test_data[col] = safe_label_encode(test_data[col], le)

    test_data_scaled = scaler.transform(test_data)

    predictions = model.predict(test_data_scaled)

    return bool(predictions)