import streamlit as st
import pandas as pd
import joblib

# Load trained model and label encoder
model = joblib.load("traffic_model.pkl")
encoder = joblib.load("label_encoder.pkl")

st.set_page_config(page_title="Smart Traffic LED Control", layout="centered")
st.title("🚦 Smart Traffic Light Controller (2 Roads + RGB LED)")
st.markdown("Use ultrasonic sensor data from Road 1 or Road 2 and let the system decide the signal color.")

# Select road currently being monitored
monitored_road = st.selectbox("Which road is the ultrasonic sensor facing?", ["Road 1", "Road 2"])

# User inputs
vehicle_count = st.slider("Vehicle Count", 0, 300, 80)
avg_speed = st.slider("Average Speed (km/h)", 0, 100, 35)
density = st.slider("Vehicle Density (%)", 0, 100, 50)
vehicle_type_count = st.slider("Types of Vehicles Detected", 1, 5, 3)

# Simulate sensor presence value (always true since sensor is positioned)
active_road_vehicles = st.slider("Number of Vehicles Detected by Sensor", 0, 4, 2)

if st.button("Predict & Control Signal"):
    # Create input features for model
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Avg Speed (km/h)': avg_speed,
        'Vehicle Density (%)': density,
        'Active Road Vehicles': active_road_vehicles,
        'Vehicle Type Count': vehicle_type_count
    }])

    prediction = model.predict(input_data)[0]
    congestion_level = encoder.inverse_transform([prediction])[0]

    # Rule + ML Hybrid Logic
    if congestion_level == "High" or vehicle_count >= 100:
        road_signal = {monitored_road: "GREEN", "Road 1" if monitored_road == "Road 2" else "Road 2": "RED"}
    else:
        road_signal = {monitored_road: "RED", "Road 1" if monitored_road == "Road 2" else "Road 2": "GREEN"}

    st.subheader(f"🚗 Predicted Congestion: **{congestion_level}**")

    st.markdown(f"**🟩 GREEN Signal:** {', '.join([road for road, sig in road_signal.items() if sig == 'GREEN'])}")
    st.markdown(f"**🟥 RED Signal:** {', '.join([road for road, sig in road_signal.items() if sig == 'RED'])}")

    # RGB LED Simulation
    st.markdown("### 💡 RGB LED Display")
    if road_signal[monitored_road] == "GREEN":
        st.success(f"RGB LED on {monitored_road}: 🟩 Green (Go)")
    else:
        st.error(f"RGB LED on {monitored_road}: 🟥 Red (Stop)")
