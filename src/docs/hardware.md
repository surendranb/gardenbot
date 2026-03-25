# ⚙️ Hardware & Sensors Architecture

GardenOS relies on a minimal, robust hardware stack. Rather than pursuing hyper-accurate laboratory sensors, the system embraces relative motion (deltas) and uses the AI agent to correct for sensor drift via visual confirmation.

## The Microcontroller Pipeline

The core hardware is an **Arduino Uno** running a standard serial telemetry sketch. 
Every 20 minutes, a headless Python chron job (`warden.py`) wakes up, connects to `/dev/cu.usbmodem1201`, establishes a reliable serial pipeline, and captures the latest string of comma-separated variables.

This data is then appended locally to `telemetry.csv`, maintaining a flawless, low-power historical record of the biome's health.

## The Sensor Array

To avoid single-points of failure, the payload distributes its sensing logic across both capacitive and resistive hardware.

### p1: The Resistive Extremist
- **Plant**: String of Nickels (*Dischidia nummularia*)
- **Sensor Type**: Traditional two-prong Resistive
- **Why**: Resistive sensors are prone to oxidation and drift over long periods. However, because `p1` is an epiphyte that desires extreme dry cycles, the resistive sensor acts as our binary threshold monitor. If the resistive sensor reads >80%, the entire biome is adequately saturated.

### p2 - p4: The Capacitive Core
- **Plants**: Mexican Mint, Pothos, Silver Guest Alpha
- **Sensor Type**: Capacitive Soil Moisture Sensors (v1.2)
- **Why**: Capacitive sensors measure the dielectric permittivity of the soil rather than direct conductivity. They do not corrode, making them perfect for the deeply moist conditions required by `p3` (Pothos). They provide a highly stable, linear curve for tracking subtle transpiration rates over 72-hour windows.

## The Optic Anchor & OpenCV

Real-world AI vision requires absolute scale. LLMs cannot inherently tell the distance of a camera from a pot.

To solve this, the camera pipeline (`vision.py`) utilizes standard **OpenCV (`cv2`)** to capture an exact, focal-locked image of the biome. At the dead center of the frame sits the "Optic Anchor"—a pure white rabbit figurine.

Because the OpenClaw agent is explicitly told in its `GARDEN_MANIFEST` that the rabbit is exactly **50mm tall**, the vision agent can confidently measure millimeter-scale leaf expansion and apical leans, bridging the gap between flat pixels and deep telemetry.
