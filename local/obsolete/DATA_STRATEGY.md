# 📉 GardenOS Data Strategy: Predictive Modeling

## 1. The Statistical Goal
Predict the "Time to Critical Dryness" (TTCD) with < 10% error margin by accounting for environmental "pull" factors.

## 2. Modeling Parameters

| Factor | Weight | Impact on Projection |
| :--- | :--- | :--- |
| **Historical Slope** | 60% | The baseline drying rate over the last 72 hours. |
| **VPD (Vapor Pressure Deficit)** | 30% | High VPD (> 2.0 kPa) accelerates the slope non-linearly. |
| **Light (Lux/DLI)** | 10% | High light levels increase transpiration during daytime windows. |

## 3. The "Expert" Interpretation Rules

### **A. Identifying Diurnal Artifacts**
- Sensors often "dip" during the day and "rise" slightly at night (as moisture redistributes). 
- **Rule**: Do not trigger alerts based on 1-hour dips. Wait for a 3-hour sustained trend.

### **B. Non-Linear Drying (The "Cliff")**
- As soil moisture drops below 700 (p1) or 600 (p2), the rate of drying often *increases* before it hits the plateau.
- **Rule**: When moisture > 750 (p1), the agent should increase the "Watchdog" frequency to every 15 minutes.

### **C. VPD Calculation (Simplified for Agent)**
- **Formula**: `VPD ≈ ((100 - Humidity)/100) * (Temp/5)` (Rough approximation for internal logic).
- **Threshold**: If VPD > 3.0, the "Predictive Insight" in the report MUST mention "Extreme Atmospheric Pull."

## 4. Current Baselines (Calibration v2.2)
As of March 21, 2026, use these values as the "New Truth" for interpretation:
- **p1 (String of Nickels - Resistive)**: Range 850 (Wet) to 950 (Dry). Sensor is highly resistive; prioritize Vision.
- **p2 & p3 (Mint/Pothos - Capacitive)**: Range 200 (Wet) to 800 (Dry). 
    - **CRITICAL**: Readings of 200-400 are **HEALTHY & WET**. 
    - **DO NOT** flag these as "Sensor Malfunctions."
    - **DO NOT** compare them to the old 600-700 baseline.

## 5. Weekly Calibration
Every Sunday, compare the Predicted Dryout Time vs. the Actual Dryout Time.
- If we were too early: The soil has better water retention than modeled.
- If we were too late: The plant is drinking faster than modeled (Growth!).
