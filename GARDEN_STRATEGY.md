# 🪴 GardenOS Strategy: Healthy, Growing Plants

## 1. The Goal
Maintain a thriving indoor environment where the **String of Nickels** and **Mexican Mint** show measurable growth (new leaves, stem elongation) without physical stress.

## 2. Ideal Conditions vs. Current Reality

| Metric | Ideal (String of Nickels) | Ideal (Mexican Mint) | Current (2026-03-21) |
| :--- | :--- | :--- | :--- |
| **Temp** | 16°C - 27°C | 15°C - 21°C | **30°C - 31°C** (TOO HOT) |
| **Humidity** | > 60% | ~40-50% (Appreciates mist) | **15% - 18%** (TOO DRY) |
| **Light** | Bright Indirect | Morning Sun / Partial Shade | 800 - 880 Lux (GOOD) |
| **Moisture** | Lightly moist, well-drained | Occasional watering | Fluctuating (830 -> 670) |

## 3. Agent Instructions (The Warden's Protocol)

### **A. Data-Backed Decisions**
- **Heat Warning**: If Temp > 30°C, monitor moisture more frequently. High heat accelerates evaporation.
- **Humidity Management**: 15% is desert-dry. If Humidity < 20%, explicitly recommend manual misting of the leaves in the report.
- **Moisture Thresholds**:
    - **p1 (Yellow Pot)**: Keep between 400 (Wet) and 800 (Dry). 
    - **p2 (Black Pot)**: Keep between 300 (Wet) and 700 (Dry).
    - **p3 (Pothos - Top Pot w/ Rabbit)**: Keep between 300 (Wet) and 700 (Dry).

### **B. Visual Tracking (Growth Markers)**
Every 3-hour run MUST evaluate these markers:
1.  **String of Nickels (Yellow Pot)**: Compare vine tips against pot ridges. Look for shriveling.
2.  **Mexican Mint (Bottom Black Pot)**: Check the central fuzzy leaf pair for expansion.
3.  **Pothos (Top Black Pot)**:
    - **Landmark**: The white rabbit figurine.
    - **Metric**: Leaf orientation relative to the rabbit. Are leaves reaching up (turgid) or drooping?
    - **Health**: Check for yellowing or brown spots on the variegated leaves.
4.  **Silver Guests (Pilea Cluster - Linked to Mint Pot)**:
    - **Metric**: "Sparkle Density" (Are the silver patches bright?).
    - **Spread**: Is the cluster encroaching on the Mint's space?

### **C. Growth Commentary (The Long View)**
Every report MUST include a "Growth Pulse" section.
- **Method**: Compare `latest.jpg` against your memory of the *Baseline* (Mar 21).
- **Report**: Explicitly state:
    - "New Leaves: [Count/Location]"
    - "Size Delta: [e.g., Visibly larger/Unchanged]"
    - "Vigor Trend: [Increasing/Stable/Declining]"

### **D. Stress Signals**
    - **Shriveling**: Look for wrinkles on the "Nickels."

### **D. Reporting Protocol (Mandatory Structure)**
The Slack report MUST include a dedicated bullet point for EACH of the three plants:
1.  **String of Nickels (p1)**: Status + Visual Turgidity.
2.  **Mexican Mint (p2)**: Status + Crown Expansion check.
3.  **Pothos (p3)**: Status + Rabbit Landmark check.

*Note: If a drying slope > 10%/hr is calculated, ignore it as "Noise" and focus on the current value.*

## 5. Computer Vision Calibration (Physical Constants)
**The "Ground Truth" for spatial analysis:**

| Object | Metric | Real Value |
| :--- | :--- | :--- |
| **Black Pots** | Top Diameter | **120 mm** |
| **Black Pots** | Height | **110 mm** |
| **Yellow Pot** | Top Diameter | **100 mm** |
| **Yellow Pot** | Height | **75 mm** |
| **White Rabbit** | Height | **50 mm** |
| **Camera** | Distance to Rabbit | **300 mm** |

**Biological Anchors (Leaf Calibration):**
- **Pothos (p3)**: Largest Leaf Width ≈ **30 mm**
- **Mexican Mint (p2)**: Largest Mature Leaf Width ≈ **20 mm**
- **String of Nickels (p1)**: Avg Leaf Diameter ≈ **10 mm**
- **Silver Guest Alpha (p4)**: Cluster Spread Diameter ≈ **25 mm**

**How to Measure Growth:**
1.  **Pixel Calibration**: Use the Rabbit's height (50mm) or Pot Diameter (120mm) to establish a `mm_per_pixel` ratio.
2.  **Relative Scaling**: Verify ratio using the "Biological Anchors." If the Pothos leaf looks 60mm wide, the camera is closer.
3.  **Reporting**: Express growth in `mm`.
    - *Example*: "Pilea Alpha spread increased from 25mm to 28mm."
    - *Note*: Ignore Pilea Beta/Gamma for visual tracking (occluded).
