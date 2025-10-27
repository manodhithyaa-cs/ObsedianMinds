import requests
import json

print("🔍 Fetching live contamination risk for multiple Indian water bodies...\n")

BASE_URL = "http://127.0.0.1:5000/api/batch_predict"

water_bodies = [
    # 🌊 Beaches
    "Marina Beach, Chennai",
    "Juhu Beach, Mumbai",
    "Baga Beach, Goa",
    "Varkala Beach, Kerala",
    "Elliot Beach, Chennai",
    "Kovalam Beach, Trivandrum",
    "Puri Beach, Odisha",
    "Digha Beach, West Bengal",
    "Rishikonda Beach, Visakhapatnam",
    "Tarkarli Beach, Maharashtra",

    # 🏞️ Lakes
    "Dal Lake, Srinagar",
    "Chilika Lake, Odisha",
    "Vembanad Lake, Kerala",
    "Loktak Lake, Manipur",
    "Sambhar Lake, Rajasthan",
    "Hussain Sagar, Hyderabad",
    "Upper Lake, Bhopal",
    "Kodaikanal Lake, Tamil Nadu",
    "Naini Lake, Nainital",
    "Pulicat Lake, Tamil Nadu",

    # 🌅 Rivers
    "Ganga River, Varanasi",
    "Yamuna River, Delhi",
    "Brahmaputra River, Guwahati",
    "Godavari River, Nashik",
    "Krishna River, Vijayawada",
    "Cauvery River, Mysuru",
    "Sabarmati River, Ahmedabad",
    "Mahanadi River, Cuttack",
    "Periyar River, Kerala",
    "Teesta River, Sikkim"
]

# Send them as multiple query params (not a single comma-separated string)
params = [("locations", wb) for wb in water_bodies]
params.append(("days", 90))

response = requests.get(BASE_URL, params=params)

try:
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # save output to JSON file
    with open("batch_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("\n✅ Results saved to batch_results.json")

except Exception as e:
    print("❌ Error parsing response:", e)
    print("Raw response:", response.text)
