# main.py
import os
import requests
from dotenv import load_dotenv
import math, time, datetime, json, numpy as np

load_dotenv()

# Load env vars
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENMETEO_API_URL = os.getenv("OPENMETEO_API_URL", "https://api.open-meteo.com/v1/forecast")

# Sanity check
if not all([OPENWEATHER_API_KEY, OPENMETEO_API_URL]):
    print("⚠️ Missing required environment variables.")


# ---------------- LOCATION FETCH ---------------- #
def get_coordinates(location: str):
    """Get coordinates strictly within India. Uses OpenWeather first, falls back to OpenStreetMap."""
    INDIA_BOUNDS = {"lat_min": 6.0, "lat_max": 37.5, "lon_min": 68.0, "lon_max": 97.5}

    def within_india(lat, lon):
        return (
            INDIA_BOUNDS["lat_min"] <= lat <= INDIA_BOUNDS["lat_max"]
            and INDIA_BOUNDS["lon_min"] <= lon <= INDIA_BOUNDS["lon_max"]
        )

    # Try OpenWeather geocoding first
    try:
        res = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={"q": location, "limit": 3, "appid": OPENWEATHER_API_KEY},
            timeout=6
        )
        data = res.json()

        for d in data:
            lat, lon = float(d["lat"]), float(d["lon"])
            country = d.get("country", "")
            if country == "IN" or within_india(lat, lon):
                return round(lat, 6), round(lon, 6)
        print("⚠️ No valid Indian coordinate found from OpenWeather, using OSM fallback...")
    except Exception:
        print("⚠️ OpenWeather geocode failed, using OSM...")

    # Fallback to OpenStreetMap (India only)
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": location,
                "countrycodes": "in",
                "format": "json",
                "limit": 1
            },
            headers={"User-Agent": "AquaScope/1.0"},
            timeout=6
        )
        d = r.json()
        if d:
            lat, lon = float(d[0]["lat"]), float(d[0]["lon"])
            if within_india(lat, lon):
                return round(lat, 6), round(lon, 6)
    except Exception:
        pass

    raise ValueError(f"❌ Invalid or out-of-India location: {location}")



# ---------------- WEATHER DATA ---------------- #
def get_openweather_current(lat, lon):
    """Fetch current weather data from OpenWeather."""
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=6
        )
        w = r.json()
        return {
            "clouds": float(w["clouds"]["all"]),
            "humidity": float(w["main"]["humidity"]),
            "pressure": float(w["main"]["pressure"]),
            "temperature": float(w["main"]["temp"]),
            "visibility": int(w.get("visibility", 10000)),
            "wind_speed": float(w["wind"]["speed"]),
        }
    except Exception as e:
        print("⚠️ OpenWeather fetch failed:", e)
        return {"clouds": 0, "humidity": 0, "pressure": 0, "temperature": 0, "visibility": 0, "wind_speed": 0}


def get_openmeteo_historical(lat, lon, days=90):
    """Historical weather aggregates from Open-Meteo."""
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days)
    try:
        r = requests.get(
            OPENMETEO_API_URL.replace("forecast", "archive"),
            params={
                "latitude": lat,
                "longitude": lon,
                "start_date": start.isoformat(),
                "end_date": today.isoformat(),
                "daily": "temperature_2m_mean,precipitation_sum,windspeed_10m_max",
                "timezone": "auto",
            },
            timeout=8
        )
        data = r.json().get("daily", {})
        temps = data.get("temperature_2m_mean", [])
        precs = data.get("precipitation_sum", [])
        winds = data.get("windspeed_10m_max", [])
        mean_temp = float(np.mean(temps)) if temps else 0
        sum_precip = float(np.sum(precs)) if precs else 0
        mean_wind = float(np.mean(winds)) if winds else 0
        temp_trend = float(temps[-1] - temps[0]) if len(temps) >= 2 else 0
    except Exception:
        mean_temp = sum_precip = mean_wind = temp_trend = 0

    return {
        "hist_mean_temp": round(mean_temp, 2),
        "hist_sum_precip": round(sum_precip, 3),
        "hist_mean_wind": round(mean_wind, 2),
        "hist_temp_trend": round(temp_trend, 2),
    }


# ---------------- SATELLITE & ENVIRONMENT DATA ---------------- #
def get_copernicus_marine(lat, lon):
    """Fetch chlorophyll, salinity, turbidity (surface-level) from Copernicus Marine API."""
    try:
        r = requests.get(
            "https://marine.copernicus.eu/api/v1/nrt-data",
            params={
                "latitude": lat,
                "longitude": lon,
                "variables": "chl,sal,turb",
                "depth": 0,
            },
            timeout=10
        )
        d = r.json()
        chl = d.get("chl", 0.4)
        sal = d.get("sal", 35.0)
        turb = d.get("turb", 1.0)
    except Exception:
        chl, sal, turb = 0.4, 35.0, 1.0
    return {"chlorophyll": chl, "salinity": sal, "turbidity": turb}


def get_nasa_power(lat, lon):
    """Fetch environmental surface data like solar radiation and soil moisture."""
    try:
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
        r = requests.get(url, params={
            "parameters": "ALLSKY_SFC_SW_DWN,SOILM_TOT",
            "community": "RE",
            "longitude": lon,
            "latitude": lat,
            "start": (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y%m%d"),
            "end": datetime.date.today().strftime("%Y%m%d"),
            "format": "JSON"
        }, timeout=10)
        data = r.json()["properties"]["parameter"]
        rad = np.mean(list(data["ALLSKY_SFC_SW_DWN"].values()))
        soil = np.mean(list(data["SOILM_TOT"].values()))
    except Exception:
        rad, soil = 180, 0.25
    return {"solar_rad": round(rad, 2), "soil_moist": round(soil, 3)}


def compute_satellite_indices(lat, lon, chl, sal, turb):
    """Compute NDWI & NDTI from marine parameters (simulated physically-based)."""
    ndwi = round(0.6 - 0.002 * turb + 0.001 * (35 - abs(35 - sal)), 3)
    ndti = round(0.4 + 0.005 * turb + 0.001 * chl, 3)
    ndwi = max(-1, min(1, ndwi))
    ndti = max(-1, min(1, ndti))
    return {"ndwi": ndwi, "ndti": ndti}


# ---------------- MASTER FUNCTION ---------------- #
def get_live_features(location, past_days=90):
    lat, lon = get_coordinates(location)

    current = get_openweather_current(lat, lon)
    hist = get_openmeteo_historical(lat, lon, days=past_days)
    marine = get_copernicus_marine(lat, lon)
    nasa = get_nasa_power(lat, lon)
    indices = compute_satellite_indices(lat, lon, marine["chlorophyll"], marine["salinity"], marine["turbidity"])

    features = {
        "lat": lat,
        "lon": lon,
        "temp": current["temperature"],
        "humidity": current["humidity"],
        "wind_speed": current["wind_speed"],
        "precip": hist["hist_sum_precip"],
        "ndwi": indices["ndwi"],
        "ndti": indices["ndti"],
        "hist_mean_temp": hist["hist_mean_temp"],
        "hist_mean_wind": hist["hist_mean_wind"],
        "hist_temp_trend": hist["hist_temp_trend"],
        "aqi": 2,  # dummy since we don’t fetch air pollution here
        "clouds": current["clouds"],
        "pressure": current["pressure"],
        "visibility": current["visibility"],
        "solar_rad": nasa["solar_rad"],
        "soil_moist": nasa["soil_moist"]
    }
    return features

# Bettina
# ---------------- SATELLITE IMAGES ---------------- #
def get_satellite_image(lat, lon, zoom=8, size="600x600", map_type="satellite", api_key=None):
    """
    Fetch satellite image of a location using Google Maps Static API.
    Args:
        lat, lon: Coordinates
        zoom: Zoom level (1-20)
        size: Image size (WxH)
        map_type: 'satellite', 'roadmap', 'terrain', 'hybrid'
        api_key: Your Google Maps API key
    Returns:
        Image bytes
    """
    if not api_key:
        print("No Google Maps API key provided, cannot fetch satellite image.")
        return None

    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": size,
        "maptype": map_type,
        "key": api_key
    }

    try:
        import requests
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.content  # You can save this as an image file
        else:
            print(f"Failed to fetch satellite image: {response.status_code}")
    except Exception as e:
        print("Error fetching satellite image:", e)
        return None


def save_satellite_image(lat, lon, filename="sat_image.png", api_key=None):
    """Fetch and save satellite image locally."""
    img_bytes = get_satellite_image(lat, lon, api_key=api_key)
    if img_bytes:
        with open(filename, "wb") as f:
            f.write(img_bytes)
        print(f"Satellite image saved as {filename}")
        return filename
    return None
def get_live_features_with_image(location, past_days=90, google_api_key=None):
    features = get_live_features(location, past_days=past_days)
    
    # Fetch satellite image
    img_file = save_satellite_image(features["lat"], features["lon"], api_key=google_api_key)
    features["satellite_image"] = img_file  # path to saved image
    
    return features
