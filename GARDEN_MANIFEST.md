# 🪴 GardenOS: Master Manifest

## 1. THE MISSION (Why)
To maintain a thriving indoor garden on a desk in Chennai, India, where ambient temperatures exceed 30°C and humidity is desert-dry (<25%). The goal is to track subtle growth markers (mm-scale) and ensure plant health through manual intervention.

## 2. THE SETUP (What & Who)
- **The Human**: Surendran. He performs all watering, misting, and physical care.
- **The System**: GardenOS (Warden & Observer).
- **The Location**: Indoor desk-top.
- **Automation**: **ZERO**. There are no pumps or timed valves.
- **Ground Truth**: Visuals supersede sensors. If a sensor says "Dry" but leaves are "Turgid" in `latest.jpg`, the sensor is lying.

## 3. PLANT REGISTRY (The Targets)
*Tracking focused on p1, p2, p3, and p4. p2 and p4 share sensor A5.*

| ID | Name | Species | Sensor | Dry Threshold | Color | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| **p1** | String of Nickels | *Dischidia nummularia* | Resistive (A0) | 15% | #00FF41 | Sensor noisy/suspect. |
| **p2** | Mexican Mint | *Plectranthus amboinicus*| Capacitive (A5) | 20% | #ADFF2F | Primary sensor for p2 and p4. |
| **p3** | Pothos | *Epipremnum aureum* | Capacitive (A2) | 20% | #FFD700 | Primary growth target. |
| **p4** | Silver Guest Alpha | *Pilea glaucophylla* | Capacitive (A5) | 30% | #C0C0C0 | Physical plant in the same pot as Mexican Mint (p2), shares sensor A5. |

## 4. PHYSICAL CONSTANTS (Calibration)
*Established March 21, 2026. Use for mm-scale growth analysis:*
- **White Rabbit Figurine**: **50 mm** (Primary Scale Anchor for visual analysis).
- **Black Pots (p2, p3)**: 120mm Diameter / 110mm Height.
- **Yellow Pot (p1)**: 100mm Diameter / 75mm Height.
- **Pothos Mature Leaf Width**: ~30 mm.
- **Mexican Mint Mature Leaf Width**: ~20 mm.

## 5. THE OBSERVER PROTOCOL (How)
### **Standard Analysis Loop (Every 3 Hours)**
1.  **Gather**: Read context from `GARDEN_MANIFEST.md` and `data/observer_context.md`. Analyze `media/latest.jpg`. Reference last 3 entries of `logs/vision_ledger.md`.
2.  **Vitality Check**: Focus visual audit on **p1, p2, p3, and p4**. Check for wilting, drooping, or color changes. Compare visual state to sensor readings in `observer_context.md`.
3.  **Log Findings**: Append to `logs/vision_ledger.md` (## YYYY-MM-DD HH:MM format).
4.  **Report**: Post Slack report to `#plantclaw` (ID: `C0AK6A4SJES`) with attachments.

### **Daily Growth Analysis (06:00 AM ONLY)**
*   **Trigger**: If the current run is at 06:00 AM.
*   **Task**: Compare `media/latest.jpg` (TODAY'S baseline) with a photo from **exactly 24 hours ago**.
*   **Locating Yesterday's Photo**: Look in the directory `archive/[YESTERDAY'S_DATE]/`. Find the file starting with `garden_0600*.jpg`. Use the most recent file in that range.
*   **Measurement**: Use the "White Rabbit" (50mm) as a scale anchor. Estimate mm growth for Pothos (p3) and Mexican Mint (p2).
*   **Report**: Include a detailed "Growth Pulse" section in the Slack report, stating mm delta, vigor trend, and any new leaves observed.

### **Slack Report Structure**
*   **Header**: `🔭 _3-HOUR GARDEN OBSERVER REPORT_ (YYYY-MM-DD HH:MM)`
*   **Biometric Status**: Bullet points for p1-p4 (e.g., `• p1: 🟢 NOMINAL (15%)`).
*   **Visual Interpretation**: Detailed observations for p1-p4. Vitality check is paramount.
*   **Growth Pulse** (06:00 AM Only): explicit growth metrics. Otherwise, state "Monitoring".
*   **Action**: ---
 
 ## 6. WORLD MODEL (The Biome)
 *Codified March 27, 2026. Use for semantic reasoning/divergence analysis.*
 
 ### **A. LIGHTING GEOMETRY**
 - **Primary Window**: North-facing, 2m distance. Diffuse, stable light. Low UV-index.
 - **Wall Orientation**: Plants against East-facing wall. No direct morning sun entry (wall-shielded).
 - **Camera LED**: Always ON. Provides persistent cool-spectrum fill light.
 
 ### **B. ATMOSPHERIC MICROCLIMATE**
 - **Thermal Ceiling**: 26°C (When AC is active). AC is located farthest from the North window.
 - **Convection**: Two ceiling fans (2m above, 1m lateral). High air exchange; prevents stagnant boundary layers.
 - **Thermal Gain**: Room is on the 1st floor with an open terrace above. Expect solar-thermal radiation through the ceiling during peak hours (12:00-15:00).
 
 ### **C. PHYSICAL LAYOUT**
 - **Desk Surface**: Wooden (Insulating). Low thermal conduction from desk to pots.
 - **Spatial Density**: P2, P3, and P4 are clustered in a single black pot (sharing resources/shading). P1 is isolated in a smaller yellow pot.
 
 ### **D. HUMAN FACTOR**
 - **Occupancy**: Human present 09:00 - 23:00 daily (12+ hours).
 - **Impact**: Localized CO2 enrichment and thermal mass (body heat) within 1m of the desk.
 
 ### **E. HYPOTHESIS-DRIVEN CARE**
 - **Spike Analysis**: If Soil % jumps without recorded care, infer **Misting** or **User-led Watering**.
 - **VPD Divergence**: Expect indoor humidity to be 30-40% lower than "Misty" outdoor forecasts due to AC dehumidification.