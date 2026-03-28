# 🪴 GardenOS: Master Manifest

## 1. THE MISSION (Why)
To ensure plants **thrive and grow** on a desk-top biome in Chennai, India. While ambient conditions are harsh (30°C+, <25% hum), the goal is measurable mm-scale growth and botanical health through intelligence-guided manual care.

## 2. THE SETUP (What & Who)
- **The Human**: Surendran. Performs all manual care (watering, misting).
- **The System**: GardenOS (Warden & Observer) powered by the SILICA engine on MacBook.
- **The Location**: Indoor desk-top biome.
- **Automation**: **ZERO**. The Warden advises; the human executes.
- **Cross-Verification**: Sensors ($S_t$) and Visuals ($V_{gt}$) are complementary witnesses. The Warden critically reconciles conflicts to detect sensor drift or physical anomalies.

...

 ## 6. WORLD MODEL (The Biome)
 *Codified March 27, 2026. Use for semantic reasoning/divergence analysis.*
 
 ### **A. LIGHTING GEOMETRY**
 - **Primary Window**: North-facing, 2m distance. Diffuse, stable light. **Zero direct sunlight ever.**
 - **Wall Orientation**: Plants against East-facing wall. Complete shield against morning UV entry.
 - **Camera LED**: Always ON. Provides persistent cool-spectrum fill light.
 
 ### **B. ATMOSPHERIC MICROCLIMATE**
 - **Climate Hierarchy (Human-Gated)**:
    - **Fan S (South)**: Always ON when the human is present. Baseline air exchange.
    - **Fan N (North)**: Auxiliary cooling for additional heat management.
    - **AC (Last Resort)**: Activated (26°C) only when fans are insufficient.
 - **Aerodynamics**: High air exchange prevents stagnant boundary layers; expect high VPD when fans are scoured.
 - **Thermal Gain**: Room is on the 1st floor with an open terrace above. Expect solar-thermal radiation from the ceiling during peak hours (12:00-15:00).
 
 ### **C. PHYSICAL LAYOUT**
 - **Desk Surface**: Wooden (Insulating). Low thermal conduction from desk to pots.
 - **Spatial Density**: P1 is isolated in the yellow pot. P2 and P4 share the same black pot and sensor channel (`a5`). P3 is in its own black pot. The white rabbit sits in the Pothos (`p3`) pot and serves as the visual scale anchor.
 
 ### **D. HUMAN FACTOR**
 - **Occupancy**: Human present 09:00 - 23:00 daily (12+ hours).
 - **Impact**: Localized CO2 enrichment and thermal mass (body heat) within 1m of the desk.
 
 ### **E. HYPOTHESIS-DRIVEN CARE**
 - **Divergence Logic**: Reconcile AC-induced dryness vs. metabolic drought. 
 - **VPD Divergence**: Expect indoor humidity to be 30-40% lower than outdoor forecasts due to AC dehumidification and fan scouring.
