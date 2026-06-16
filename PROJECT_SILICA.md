# 🌿 Project SILICA: The Garden Warden Master Ledger

Project SILICA is the centralized biological and technical intelligence framework for the Gardenbot biome. It serves as the single source of truth for both the AI Warden and the system's operational parameters.

---

## 1. THE MISSION & PERSONA
- **The Mission**: To help a single Jade plant thrive in a high-VPD indoor environment in Chennai through intelligence-led manual care.
- **The Persona**: An expert agricultural statistician with a specialty in tropical meteorology. 
- **Core Philosophy**: "Local Truth over Textbook Guesses." Prioritize visual turgidity, deterministic math (Vapor Pressure Deficit), and acoustic ground-truth over raw sensor alarms.

---

## 2. THE WORLD MODEL (The Biome)
- **Lighting**: North-facing window (diffuse light only). Camera LED always ON for calibration.
- **Microclimate**: 
    - **Thermal Gain**: 12:00 - 15:00 from ceiling radiation (1st floor). 
    - **Airflow**: 
        - **Fan S (South)**: Primary convection.
        - **Fan N (North)**: Auxiliary cooling.
        - **AC**: Last resort at 26°C (Note: Tanks humidity, spikes VPD).
- **Physical Layout**: 
    - **One plant**: Jade Plant / Crassula ovata (Black Pot | Soil moisture sensor | Indoor desk).
    - **Unmonitored**: Self-Watering Pot (White Cylindrical Object in Background | Pending Setup).

## 2.5. BIOLOGICAL BASELINE 
**Jade Plant (Crassula ovata)**
- **Care Type**: Succulent.
- **Watering Strategy**: Strict "Soak and Dry". Because it is currently in a shallow dish lacking drainage, watering must be extremely conservative to prevent root rot. Allow soil to dry completely before watering.
- **Visual Turgidity**: Healthy leaves are firm, plump, and upright. Underwatered leaves become soft, wrinkled, or flat. Overwatered leaves may turn yellow and drop off easily.
- **VPD Goal**: High. Tolerates dry indoor atmospheres well (0.8 kPa to 1.5 kPa or higher). Low humidity prevents fungal diseases.

---

## 3. HARDWARE HARDENING (Sentinel-1 / v3.3)
To prevent I2C signal dropouts and "disturbed" telemetry, the following physical constants are mandatory:

- **I2C Address**: The BME680 is hard-locked at **`0x76`**.
- **Physical Mounting**: The sensor is directly wired/mounted (No breadboard). Ensure every pin has secure electrical contact and isolation.
- **Boot Protocol**: A **3.0s settle delay** must be executed before I2C initialization to prevent race conditions.
- **Loop Delay**: Production loop is set to **5.0s** to preserve the BME680 heater's lifespan.

---

## 4. SYSTEM ARCHITECTURE
The system is decoupled into four functional layers:

1. **Collection (`launchd`)**: `pulse.sh` runs every 30m. `warden.py` captures sensor data from the Arduino.
2. **Context (SILICA)**: `prep_observer_context.py` synthesizes telemetry, vision observation, and human actions into `data/observer_context.md`.
3. **Reasoning (OpenClaw)**: The Warden (Agent) reconciles data conflicts every 4 hours and broadcasts targeted action plans.
4. **Sharing (Sync)**: `sync.sh` builds the MkDocs site and commits all data to GitHub Pages.

---

## 5. DASHBOARD & TELEMETRY SOP
- **Layout**: Single-Column Vertical Stack (one graph per line).
- **Metric Priority**: VPD (Vapor Pressure Deficit) is the primary stress indicator.
- **Real-time Truth**: All GitHub Raw data fetches MUST use cache-busting (**`?t=Date.now()`**) to bypass the 5-minute CDN delay.

---
*Last Hardened: June 16, 2026 (Cleaned legacy multi-plant references)*

---

## 6. PROJECT MANAGEMENT & TICKETING (Multica)
- **Primary Tracker**: All major architectural outcomes, hardware diagnostics, and agent adjustments must be documented in the core Multica project to preserve historical context and enable rollbacks.
- **Multica Project URL**: `http://localhost:3010/projects/61f63933-34be-4647-b71e-809493de6232`
- **Project ID**: `61f63933-34be-4647-b71e-809493de6232`
