# model.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class AquaScopeModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42)
        self._is_trained = False

    def train_dummy(self, n_samples: int = 1500, random_seed: int = 42):
        rng = np.random.RandomState(random_seed)
        temps = rng.uniform(5, 35, size=n_samples)
        humidity = rng.uniform(30, 95, size=n_samples)
        wind = rng.uniform(0, 25, size=n_samples)
        precip = rng.uniform(0, 300, size=n_samples)
        ndwi = rng.uniform(-0.2, 0.8, size=n_samples)
        ndti = rng.uniform(-0.2, 1.0, size=n_samples)
        hist_temp = temps + rng.normal(0, 2, size=n_samples)
        hist_wind = wind + rng.normal(0, 1, size=n_samples)
        temp_trend = rng.normal(0, 2, size=n_samples)
        aqi = rng.randint(1, 5, size=n_samples)
        solar = rng.uniform(100, 300, size=n_samples)
        soil = rng.uniform(0.1, 0.5, size=n_samples)

        X = np.vstack([temps, humidity, wind, precip, ndwi, ndti, hist_temp,
                       hist_wind, temp_trend, aqi, solar, soil]).T

        y = (
            25 + 0.9*temps + 0.6*humidity + 0.3*precip/10.0
            + 18*ndti - 22*ndwi + 6*(aqi-1) - 0.05*solar + 40*soil
            + rng.normal(0, 8, size=n_samples)
        )
        y = np.clip(y, 0, 100)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
        self.model.fit(X_train, y_train)
        self._is_trained = True

    def predict(self, features: dict):
        if not self._is_trained:
            self.train_dummy()
        arr = np.array([[
            features.get("temp", 0.0),
            features.get("humidity", 0.0),
            features.get("wind_speed", 0.0),
            features.get("precip", 0.0),
            features.get("ndwi", 0.0),
            features.get("ndti", 0.0),
            features.get("hist_mean_temp", 0.0),
            features.get("hist_mean_wind", 0.0),
            features.get("hist_temp_trend", 0.0),
            features.get("aqi", 0),
            features.get("solar_rad", 200),
            features.get("soil_moist", 0.25)
        ]])
        risk = float(self.model.predict(arr)[0])
        label = "🚨 High Risk" if risk >= 75 else "⚠️ Moderate Risk" if risk >= 50 else "✅ Low Risk"
        return {"Water Contamination Risk Score (%)": round(risk, 1), "Risk Label": label}
