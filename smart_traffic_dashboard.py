# smart_traffic_dashboard.py

import streamlit as st
import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("traffic_model.pkl")
encoder = joblib.load("label_encoder.pkl")

st.set_page_config(page_title="Smart Traffic Signal", layout="centered")
st.title("🚦 Smart Traffic Light Controller (2 Roads)")
st.markdown("Reposition the sensor to Road 1 or Road 2 and input data below.")

# Select road for current monitoring
current_road = st.selectbox("Select Road Being Monitored (Sensor Facing)", ["Road 1", "Road 2"])

# Input sensor data
vehicle_count = st.slider("Vehicle Count on selected road", 0, 300, 80)
avg_speed = st.slider("Average Speed (km/h)", 0, 100, 35)
density = st.slider("Vehicle Density (%)", 0, 100, 50)
vehicle_type_count = st.slider("Types of Vehicles Detected", 1, 5, 3)

# Lane-based IR logic replaced with ultrasonic presence density logic
# Fixed single-sensor use

if st.button("Update Signal Decision"):
    # Input for model
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Avg Speed (km/h)': avg_speed,
        'Vehicle Density (%)': density,
        'Lane_1': 1,  # Assuming at least 1 active IR beam replaced with ultrasonic logic
        'Lane_2': 0,
        'Lane_3': 0,
        'Lane_4': 0,
        'Vehicle Type Count': vehicle_type_count
    }])

    prediction = model.predict(input_data)[0]
    congestion_level = encoder.inverse_transform([prediction])[0]

    # Logic: If congestion is high or count is higher, give green to current road
    if congestion_level == "High" or vehicle_count > 100:
        signal_status = {current_road: "GREEN", "Road 1" if current_road == "Road 2" else "Road 2": "RED"}
    else:
        signal_status = {current_road: "RED", "Road 1" if current_road == "Road 2" else "Road 2": "GREEN"}

    # Show Results
    st.subheader("Predicted Congestion Level: " + congestion_level)
    st.markdown(f"🚧 **{current_road}** → Signal: **{signal_status[current_road]}**")
    st.markdown(f"🛣️ Other Road → Signal: **{signal_status['Road 1' if current_road == 'Road 2' else 'Road 2']}**")

    # RGB LED visual
    st.markdown("### 💡 RGB LED Indicator")
    color = "🟩 Green" if signal_status[current_road] == "GREEN" else "🟥 Red"
    st.markdown(f"**{current_road} Light:** {color}")
