# smart_traffic_dashboard.py

import streamlit as st
import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("traffic_model.pkl")
encoder = joblib.load("label_encoder.pkl")

st.set_page_config(page_title="Smart Traffic Congestion Predictor", layout="centered")
st.title("🚦 Smart Traffic Congestion Predictor")
st.markdown("Enter real-time traffic data to predict congestion level.")

# User inputs
vehicle_count = st.slider("Vehicle Count", min_value=0, max_value=300, value=100)
avg_speed = st.slider("Average Speed (km/h)", min_value=0, max_value=120, value=40)
density = st.slider("Vehicle Density (%)", min_value=0, max_value=100, value=60)

st.subheader("IR Sensor Lane Presence (1 = Vehicle Present, 0 = Empty)")
lane_1 = st.radio("Lane 1", [0, 1], horizontal=True)
lane_2 = st.radio("Lane 2", [0, 1], horizontal=True)
lane_3 = st.radio("Lane 3", [0, 1], horizontal=True)
lane_4 = st.radio("Lane 4", [0, 1], horizontal=True)

vehicle_type_count = st.slider("Types of Vehicles Detected", min_value=1, max_value=5, value=3)

# Predict button
if st.button("Predict Congestion Level"):
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Avg Speed (km/h)': avg_speed,
        'Vehicle Density (%)': density,
        'Lane_1': lane_1,
        'Lane_2': lane_2,
        'Lane_3': lane_3,
        'Lane_4': lane_4,
        'Vehicle Type Count': vehicle_type_count
    }])
    
    pred = model.predict(input_data)[0]
    label = encoder.inverse_transform([pred])[0]
    
    st.success(f"Predicted Traffic Congestion Level: **{label}**")
