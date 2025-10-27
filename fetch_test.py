import requests
import json
import time

# Flask endpoint
BASE_URL = "http://127.0.0.1:5000/analyze"

# List of locations (India + Abroad)
LOCATIONS = [
    "Elliot Beach, Chennai",
    "Marina Beach, Chennai",
    "Juhu Beach, Mumbai",
    "Varkala Beach, Kerala",
    "Chilika Lake, Odisha",
    "Bondi Beach, Sydney",
    "Copacabana Beach, Rio de Janeiro",
    "Waikiki Beach, Honolulu",
    "Venice Beach, Los Angeles",
    "Lake Geneva, Switzerland",
    "Tokyo, Japan"
]

def fetch_data(location: str):
    try:
        response = requests.get(BASE_URL, params={"location": location}, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("\n=============================================")
        print(f"🌍 Location: {location}")
        print("---------------------------------------------")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("---------------------------------------------")
        return data
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching data for {location}: {e}")
        return None

def main():
    print("=============================================")
    print("🌊 Starting Environmental Risk Fetch Test")
    print("=============================================")

    results = []

    for loc in LOCATIONS:
        data = fetch_data(loc)
        if data:
            results.append(data)
        time.sleep(2)  # small delay between requests

    # Save all fetched results to a file
    with open("fetched_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n=============================================")
    print("✅ Done fetching all locations!")
    print("🌐 Results saved to fetched_results.json")
    print("=============================================")


if __name__ == "__main__":
    main()
