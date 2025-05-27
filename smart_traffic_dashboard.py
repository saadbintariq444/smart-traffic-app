# Button to make prediction and control signal
if st.button("Predict & Control Signal"):
    # ✅ Corrected: Only include expected features
    input_data = pd.DataFrame([{
        'Vehicle Count': vehicle_count,
        'Active Road Vehicles': active_road_vehicles
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
