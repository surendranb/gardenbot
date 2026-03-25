# The Gardenbot Setup

*March 20, 2026*

GardenOS is a monitoring system designed to track the health of an indoor tropical desk-top biome in Chennai, India, where ambient temperatures regularly exceed 30°C and humidity often drops below 25%. The primary purpose of this system is to provide actionable intelligence for manual plant care, operating entirely without automated pumps or valves.

## The Plant Registry

The system monitors four specific botanical targets:

1.  **p1 (String of Nickels / Dischidia nummularia)**: A drought-tolerant epiphyte monitored via a resistive moisture sensor (A0). It serves as the indicator for extreme dry conditions.
2.  **p2 (Mexican Mint / Plectranthus amboinicus)**: A fleshy, fast-growing herb monitored via a capacitive sensor (A5). It provides clear visual indicators of turgidity and wilting.
3.  **p3 (Pothos / Epipremnum aureum)**: The primary growth target in the biome, monitored via a capacitive sensor (A2).
4.  **p4 (Silver Guest Alpha / Pilea glaucophylla)**: A secondary indicator plant sharing the same pot and sensor (A5) as the Mexican Mint.

## The Hardware and Telemetry Stack

The environment is continuously tracked using a suite of hardware sensors. The system logs raw data (`telemetry.csv`) every 20 minutes, which includes:

- **Atmospheric Data**: Temperature (°C) and Humidity (%).
- **Soil Moisture**: Percentage saturation for each individual sensor.
- **Ambient Light**: Measured in Lux.

This raw data is then processed to calculate derived metrics (`metrics.csv`), specifically Vapor Pressure Deficit (VPD), which helps determine the rate of transpiration and overall thermal stress on the plants.

## The Observer Protocol

Rather than relying purely on sensor data—which can be compromised by soil shifting or sensor oxidation—GardenOS employs a "Visuals Supersede Sensors" philosophy.

Every three hours, a wide-angle camera captures the biome (`latest.jpg`). Using a 50mm White Rabbit figurine as a physical scaling anchor, an automated Observer agent reviews the image. It compares the current visual state of the plants (turgidity, drooping, necrosis) against historical baselines and telemetry, producing a deterministic agricultural verdict logged to both a persistent markdown ledger and a Slack channel.

## Future Improvements

While this setup successfully acts as an early warning system, future iterations will focus on advancing the intelligence of the Observer agent. We intend to shift from flat-file procedural reporting toward a semantic, Vector-based episodic memory architecture. By giving the agent a historical sense of visual anomalies and a formal ontology of the biome, we aim to transition the system from a reactive monitor to a proactive, highly capable digital familiar.
