import streamlit as st
import pandas as pd
import joblib

# Load the trained model and label encoder
model = joblib.load("traffic_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Traffic Controller", layout="centered")
st.title("🚦 Smart Traffic Density Estimator")
st.markdown("👋 This system uses **1 ultrasonic sensor** that you reposition to monitor either **Road 1** or **Road 2**.")

# --- Input Section ---
monitored_road = st.selectbox("🛣️ Sensor currently facing:", ["Road 1", "Road 2"])

vehicle_count = st.slider("🚗 Estimated Total Vehicle Count on Road", 0, 300, 80)
active_road_vehicles = st.slider("📡 Vehicles Detected by Sensor Now", 0, 4, 2)

# --- Prediction & Control Logic ---
if st.button("🔍 Predict & Control Signal"):
    # Create input DataFrame with matching features
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Active Road Vehicles': active_road_vehicles
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]
    congestion_level = encoder.inverse_transform([prediction])[0]

    # Decide traffic light signal
    if congestion_level == "High" or vehicle_count >= 100:
        road_signal = {monitored_road: "GREEN", "Road 1" if monitored_road == "Road 2" else "Road 2": "RED"}
    else:
        road_signal = {monitored_road: "RED", "Road 1" if monitored_road == "Road 2" else "Road 2": "GREEN"}

    # --- Display Results ---
    st.subheader(f"🚦 Predicted Congestion: **{congestion_level}**")
    st.markdown(f"🟩 **GREEN Signal:** {', '.join([r for r, s in road_signal.items() if s == 'GREEN'])}")
    st.markdown(f"🟥 **RED Signal:** {', '.join([r for r, s in road_signal.items() if s == 'RED'])}")

    # RGB LED logic simulation
    st.markdown("### 💡 RGB LED Indicator")
    if road_signal[monitored_road] == "GREEN":
        st.success(f"✅ RGB LED on {monitored_road}: 🟢 Green (Traffic Allowed)")
    else:
        st.error(f"⛔ RGB LED on {monitored_road}: 🔴 Red (Traffic Stopped)")

# --- Footer ---
st.markdown("---")
st.markdown("Made by **Saad Bin Tariq & Amir Saeed** 🚀")
