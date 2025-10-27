# app.py  
import streamlit as st
from main import get_coordinates, get_weather_pollution
from model import predict

st.set_page_config(page_title="AquaScope", page_icon="🌊", layout="centered")
st.title("🌊 AquaScope – Live Water Contamination Risk Predictor")

st.markdown("Enter a location below to fetch live environmental data and predict contamination risk.")

location = st.text_input("📍 Location", "Elliot's Beach, Chennai")
if st.button("Analyze"):
    lat, lon = get_coordinates(location)
    if lat is None:
        st.error("❌ Could not find location.")
    else:
        st.write(f"Coordinates: {lat:.5f}, {lon:.5f}")
        KEY = "ce8c633773964a4df2c70549388c748a"
        features = get_weather_pollution(lat, lon, KEY)
        if features is None:
            st.error("⚠️ Could not fetch environmental data.")
        else:
            st.metric("Temperature (°C)", features["temperature"])
            st.metric("Humidity (%)", features["humidity"])
            st.metric("Air Quality Index (AQI)", features["aqi"])
            st.metric("Rainfall (last 1h mm)", features["rainfall"])

            pred_label, pred_prob = predict(features)
            risk_pct = round(pred_prob * 100, 1)
            st.subheader(f"🧠 Predicted Contamination Risk: {risk_pct}%")
            if pred_label == 1:
                st.error("🚨 High Risk – Potential contamination detected")
            else:
                st.success("✅ Low Risk – Water quality likely safe")

st.caption("Data provided by OpenWeatherMap • Developed by AquaScope Team")
