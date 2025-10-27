# main.py  
import requests

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    headers = {"User-Agent": "AquaScope/1.0 (manodhithyaa.cs@gmail.com)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None, None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except Exception as e:
        print("Error in get_coordinates:", e)
        return None, None

def get_weather_pollution(lat, lon, weather_api_key):
    try:
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
        )
        pollution_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution?"
            f"lat={lat}&lon={lon}&appid={weather_api_key}"
        )

        w_resp = requests.get(weather_url, timeout=10)
        p_resp = requests.get(pollution_url, timeout=10)
        w_resp.raise_for_status()
        p_resp.raise_for_status()
        w_data = w_resp.json()
        p_data = p_resp.json()

        features = {
            "temperature": w_data["main"]["temp"],
            "humidity": w_data["main"]["humidity"],
            "aqi": p_data["list"][0]["main"]["aqi"],
            # rainfall may not always appear
            "rainfall": w_data.get("rain", {}).get("1h", 0)
        }
        return features
    except Exception as e:
        print("Error in get_weather_pollution:", e)
        return None

if __name__ == "__main__":
    loc = input("Enter location: ")
    lat, lon = get_coordinates(loc)
    if lat is not None:
        print("Coords:", lat, lon)
        # Provide your OpenWeatherMap API key here
        KEY = "ce8c633773964a4df2c70549388c748a"
        feat = get_weather_pollution(lat, lon, KEY)
        print("Features:", feat)
    else:
        print("Location not found.")
