# Arid Architect: Smart Garden

Autonomous monitoring and watering system for a **String of Nickels** (succulent) using **Arduino Uno** and **Python**.

## Setup Instructions

### 1. Hardware Connections (as per Phase 1)
Follow the `wiring_guide.html` for pin mappings:
- **DHT11:** Digital Pin 2
- **Relay (Pump):** Digital Pin 3
- **HC-SR04:** Digital Pins 4 (Trig) & 5 (Echo)
- **Soil Moisture:** Analog Pin A0
- **Light Sensor:** Analog Pin A1

### 2. Software Configuration
1.  **Python Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install pyserial pillow flask
    ```
2.  **Arduino Firmware:**
    Upload `dht11_test/dht11_test.ino` to the Arduino Uno using the Arduino IDE or `arduino-cli`.

### 3. Running the System
- **Manual Pulse:** `python3 gardener_pulse.py` (reads sensors, logs data, updates dashboard).
- **Automated Pulse (Cron):**
    ```cron
    0 8,20 * * * cd /path/to/project && ./.venv/bin/python3 gardener_pulse.py
    ```
- **View Dashboard:** Open `dashboard.html` in any browser.

## Project Structure
- `gardener_pulse.py`: The core "Heartbeat" script.
- `dashboard_gen.py`: Generates the static `dashboard.html`.
- `data/garden.db`: SQLite database for long-term tracking.
- `photos/`: Directory for daily growth photos.
- `gardener.md`: The "Arid Architect's" behavioral logic and thresholds.
