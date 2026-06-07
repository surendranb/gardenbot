    health_warning = ""
    curr_temp = t_df['temp'].iloc[-1] if t_df is not None and not t_df.empty else 0
    fan_status = get_acoustic_fan_status(t_df['db'].iloc[-1] if t_df is not None and not t_df.empty else None)[0]

    if curr_temp > 36.5 and "OFF" in fan_status:
        health_warning += (
            "### 🚨 1C. CRITICAL THERMAL ALERT\n"
            f"- **TEMP**: {curr_temp}°C (Extreme Heat Spike)\n"
            "- **FANS**: OFF (Acoustic proof indicates no convection)\n"
            "- **ACTION REQUIRED**: Manually activate cooling systems immediately. VPD is likely reaching lethal thresholds for the Jade succulent.\n\n"
        )

    if failure_count > 0:
        health_warning += (
            "### ⚠️ 1D. TELEMETRY HEALTH ALERT\n"
            f"- **STATUS**: DEGRADED (Hardware Instability Detected)\n"
            f"- **FAILURE SIGNATURES DETECTED**: {failure_count} points in last window.\n"
            "- **ACTION**: Statistical windows (Section 4) have been SANITIZED. Hardware artifacts removed.\n"
            "- **CRITICAL INSTRUCTION**: If Section 5 (Vision) contradicts Section 4 (Telemetry), **TRUST THE IMAGE**. Do not hallucinate root rot if the soil is visibly dry.\n\n"
        )
