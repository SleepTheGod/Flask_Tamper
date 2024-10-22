import joblib
import numpy as np

# Load pre-trained anomaly detection model
model = joblib.load('models/anomaly_model.pkl')

def detect_anomaly(headers, body):
    # Extract features from headers and body
    features = np.array([len(headers), len(body)]).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0] == 1
