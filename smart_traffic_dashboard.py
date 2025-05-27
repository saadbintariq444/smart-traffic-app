import streamlit as st
import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("traffic_model.pkl")
encoder = joblib.load("label_encoder.pkl")

st.set_page_config(page_title="Smart Traffic Light", layout="centered")
st.title("🚦 Smart Traffic Light Controller (2 Roads + RGB LED)")
st.markdown("Move sensor to either road and enter the detected vehicle count.")

# Select the road being monitored
monitored_road = st.selectbox("Sensor currently facing:", ["Road 1", "Road 2"])

# Input from ultrasonic sensor and count estimate
vehicle_count = st.slider("Total Vehicle Count on Monitored Road", 0, 300, 80)
active_road_vehicles = st.slider("Vehicles Detected by Sensor", 0, 4, 2)

# Button to make prediction and control signal
if st.button("Predict & Control Signal"):
    # Create input features for model
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Active Road Vehicles': active_road_vehicles,
        'Vehicle Type Count': 3  # Placeholder (model expects it, will remove in retrain later)
    }])

    # Model prediction
    prediction = model.predict(input_data)[0]
    congestion_level = encoder.inverse_transform([prediction])[0]

    # Signal decision logic
    if congestion_level == "High" or vehicle_count >= 100:
        road_signal = {monitored_road: "GREEN", "Road 1" if monitored_road == "Road 2" else "Road 2": "RED"}
    else:
        road_signal = {monitored_road: "RED", "Road 1" if monitored_road == "Road 2" else "Road 2": "GREEN"}

    # Output
    st.subheader(f"🚗 Predicted Congestion: **{congestion_level}**")
    st.markdown(f"🟩 **GREEN Signal:** {', '.join([r for r, s in road_signal.items() if s == 'GREEN'])}")
    st.markdown(f"🟥 **RED Signal:** {', '.join([r for r, s in road_signal.items() if s == 'RED'])}")

    # RGB LED logic
    st.markdown("### 💡 RGB LED Indicator")
    if road_signal[monitored_road] == "GREEN":
        st.success(f"RGB LED on {monitored_road}: 🟩 Green (Go)")
    else:
        st.error(f"RGB LED on {monitored_road}: 🟥 Red (Stop)")
