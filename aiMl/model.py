# model.py  
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from main import get_coordinates, get_weather_pollution

def train_model(weather_api_key, sample_locations):
    records = []
    for loc in sample_locations:
        lat, lon = get_coordinates(loc)
        if lat is None:
            continue
        features = get_weather_pollution(lat, lon, weather_api_key)
        if features is None:
            continue
        # create synthetic label: high risk if aqi high OR humidity very high
        label = 1 if (features["aqi"] > 70 or features["humidity"] > 85) else 0
        features["risk"] = label
        records.append(features)
    df = pd.DataFrame(records)
    if df.empty:
        raise RuntimeError("No data fetched to train model.")
    X = df[["temperature", "humidity", "aqi", "rainfall"]]
    y = df["risk"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "model.pkl")
    print("Model trained and saved as model.pkl")

def predict(features):
    model = joblib.load("model.pkl")
    X = np.array([[features["temperature"], features["humidity"], features["aqi"], features["rainfall"]]])
    pred = model.predict(X)[0]
    # Optionally probability
    prob = model.predict_proba(X)[0][1]
    return pred, prob

if __name__ == "__main__":
    # Provide your OpenWeatherMap API key here
    KEY = "ce8c633773964a4df2c70549388c748a"
    sample = ["Chennai, India", "Mumbai, India", "Delhi, India", "Bangalore, India"]
    train_model(KEY, sample)
