from flask import Flask, request, jsonify
from main import get_live_features
from model import AquaScopeModel
from concurrent.futures import ThreadPoolExecutor
import traceback

app = Flask(__name__)

# Initialize model once
model = AquaScopeModel()
model.train_dummy()

# Create a small thread pool to handle multiple requests safely
executor = ThreadPoolExecutor(max_workers=5)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AquaScope – Live Prediction</title>
<style>
body {{
    font-family: Arial;
    background: #f4f9ff;
    text-align: center;
    margin-top: 60px;
}}
input {{
    padding: 10px;
    width: 340px;
    border-radius: 6px;
    border: 1px solid #aaa;
}}
button {{
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    background: #007bff;
    color: white;
    cursor: pointer;
}}
button:hover {{
    background: #0056b3;
}}
#result {{
    margin-top: 30px;
    font-size: 1.1em;
    text-align: left;
    display: inline-block;
    background: #fff;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}}
</style>
</head>
<body>
<h1>🌊 AquaScope – Water Contamination Risk Predictor</h1>
<form method="get" action="/">
  <input type="text" name="location" placeholder="Enter location (e.g. Elliot Beach, Chennai)">
  <button type="submit">Analyze</button>
</form>
<div id="result">
  {result}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    location = request.args.get("location")
    days = int(request.args.get("days", 90))
    if not location:
        return HTML_PAGE.format(result="")
    try:
        features = get_live_features(location, past_days=days)
        result = model.predict(features)
        html_result = f"""
        <p><b>Location:</b> {location}</p>
        <p><b>Latitude:</b> {features['lat']}, <b>Longitude:</b> {features['lon']}</p>
        <p><b>Temperature:</b> {features['temp']} °C</p>
        <p><b>Humidity:</b> {features['humidity']} %</p>
        <p><b>Wind Speed:</b> {features['wind_speed']} m/s</p>
        <p><b>NDWI:</b> {features['ndwi']}, <b>NDTI:</b> {features['ndti']}</p>
        <p style='font-size:1.3em;'><b>{result['Risk Label']}</b> ({result['Water Contamination Risk Score (%)']}%)</p>
        """
        return HTML_PAGE.format(result=html_result)
    except Exception as e:
        traceback.print_exc()
        return HTML_PAGE.format(result=f"<p style='color:red;'>Error: {e}</p>")

@app.route("/api/predict", methods=["GET"])
def api_predict():
    location = request.args.get("location")
    days = int(request.args.get("days", 90))
    if not location:
        return jsonify({"error": "Location required"}), 400
    try:
        features = get_live_features(location, past_days=days)
        prediction = model.predict(features)
        resp = {
            "Location": location,
            "Predicted Risk": f"{prediction['Risk Label']} ({prediction['Water Contamination Risk Score (%)']}%)",
            "aqi": features.get("aqi", 0),
            "clouds": features.get("clouds", 0),
            "humidity": features.get("humidity", 0),
            "pressure": features.get("pressure", 0),
            "rainfall": features.get("precip", 0),
            "temperature": features.get("temp", 0),
            "visibility": features.get("visibility", 0),
            "wind_speed": features.get("wind_speed", 0)
        }
        return jsonify(resp)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/batch_predict", methods=["GET"])
def api_batch_predict():
    days = int(request.args.get("days", 90))
    locs = request.args.getlist("locations")

    if not locs:
        q = request.args.get("locations")
        if q:
            locs = [l.strip() for l in q.split(",") if l.strip()]
    if not locs:
        l = request.args.get("location")
        if not l:
            return jsonify({"error": "locations (or location) query parameter required"}), 400
        locs = [x.strip() for x in l.split(",") if x.strip()]

    results = []

    def process_location(loc):
        try:
            features = get_live_features(loc, past_days=days)
            pred = model.predict(features)
            return {
                "Location": loc,
                "Predicted Risk": f"{pred['Risk Label']} ({pred['Water Contamination Risk Score (%)']}%)",
                "aqi": int(features.get("aqi", 0)),
                "clouds": float(features.get("clouds", 0)),
                "humidity": float(features.get("humidity", 0)),
                "pressure": float(features.get("pressure", 0)),
                "rainfall": float(features.get("precip", 0)),
                "temperature": float(features.get("temp", 0)),
                "visibility": int(features.get("visibility", 0)),
                "wind_speed": float(features.get("wind_speed", 0))
            }
        except Exception as e:
            return {"Location": loc, "error": str(e)}

    # Run predictions in parallel threads safely
    futures = [executor.submit(process_location, loc) for loc in locs]
    for f in futures:
        results.append(f.result())

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
