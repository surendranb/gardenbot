---
hide:
  - navigation
  - toc
---

# Hello World: The Origins of GardenOS

GardenOS wasn't built to be a simple "sensor box." It was built to be a **Curious Warden**—an agent that doesn't just read numbers, but *investigates* the biome using vision and deterministic math. This is the story of how it's set up and how it thinks.

## 🛠 The Hardware Stack
We've kept the hardware lean and focused on "Local Truth." The system is entirely local-first, avoiding cloud-dependency where possible.

*   **Brain**: An old laptop running **OpenClaw**, which serves as the primary execution environment for our agentic workflows.
*   **Controller**: An **Arduino** acting as the serial bridge for the sensor array.
*   **Atmosphere**: A **DHT11** sensor for temperature and humidity.
*   **Light**: A dedicated **Lux sensor** to track solar exposure.
*   **Soil Moisture**: Three **Capacitive Moisture Sensors** (p1: Nickels, p2: Mint, p3: Pothos). We use capacitive sensors specifically because they don't corrode like cheaper resistive ones, ensuring long-term data stability.
*   **Vision**: A standard **Webcam** mounted for top-down biome surveillance.

## 🧠 The Logical Flow
The system operates on a rigorous temporal rhythm. It doesn't just "ping" sensors; it conducts an audit.

1.  **Trigger**: A system-level `cron` job wakes the Warden every hour.
2.  **Vision Capture**: The webcam takes a high-res snap of the biome.
3.  **Sensor Audit**: The Arduino polls the DHT11, Lux, and Moisture sensors via serial.
4.  **Agent Logic**: The Warden AI analyzes the *Delta*—comparing the new photo and sensor data against the previous hour's state. It looks for "Flickers" (sudden changes), "Spatial Anomalies," and "Negative Audits" (checking if things that *should* be happening are missing).
5.  **Recording**: Findings are logged into the `telemetry.csv` and the human-readable `vision_ledger.md`.
6.  **Delivery**: A summary of the Warden's "Detective" report is sent to Slack for human oversight.

## 🌿 Final Thoughts
This setup allows GardenOS to go beyond simple "if temperature > X" logic. By correlating weather forecasts with visual turgidity and soil moisture slopes, the Warden can predict stress before it becomes visible to the human eye. 

It's not just a garden; it's a monitored biome.
