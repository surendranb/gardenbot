# 🌿 Project SILICA: The Garden Warden Master Ledger

Project SILICA is the centralized biological and technical intelligence framework for the Gardenbot biome. It serves as the single source of truth for both the AI Warden and the system's operational parameters.

---

## 1. THE MISSION & PERSONA
- **The Mission**: To ensure plants thrive in a high-VPD indoor environment in Chennai through intelligence-led manual care.
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
    - **P0**: Survivor Succulent (Tiny Yellow Pot | **THRIVING** | Vision-Only).
    - **P1**: String of Nickels (Yellow Pot | Sensor A0 | Dehydrated/Scrub).
    - **P3**: Pothos (Black Pot | Sensor A2 | White Rabbit anchor | Terminal).
    - **[RETIRED/LOST]**: 
        - **P2**: Mexican Mint (Black Pot | Systemic Loss 04-20).
        - **P4**: Silver Guest (Black Pot | Systemic Loss 04-20).

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

1. **Collection (`launchd`)**: `pulse.sh` runs every 30m. `warden.py` is prioritized for **`/dev/cu.usbmodem1201`** (Speed Hack) to ensure instantaneous capture.
2. **Context (SILICA)**: `prep_observer_context.py` synthesizes telemetry, vision observation, and human actions into `data/observer_context.md`.
3. **Reasoning (OpenClaw)**: The Warden (Agent) reconciles data conflicts every 3 hours and broadcasts targeted action plans.
4. **Sharing (Sync)**: `sync.sh` builds the MkDocs site and commits all data to GitHub Pages.

---

## 5. DASHBOARD & TELEMETRY SOP
- **Layout**: Single-Column Vertical Stack (one graph per line).
- **Metric Priority**: VPD (Vapor Pressure Deficit) is the primary stress indicator.
- **Real-time Truth**: All GitHub Raw data fetches MUST use cache-busting (**`?t=Date.now()`**) to bypass the 5-minute CDN delay.

---
*Last Hardened: April 8, 2026 (Reflecting successful BME680 recovery)*
*Operation Necropsy: April 21, 2026 (Sentinel-1 Systemic Failure identified; VGT priority enforced; world model re-baselined around survivor).*
