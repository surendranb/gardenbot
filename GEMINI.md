## 1. THE DATA & REASONING SPLIT
The system operates across a clear boundary between Local Execution and Cloud Intelligence:

- **⚙️ LOCAL (Execution & Collection)**: **OpenClaw** runs on the MacBook, executing Python scripts (`warden.py`, `vision.py`, `weather_scout.py`) to gather raw telemetry, weather data, and visual ground-truth ($V_{gt}$).
- **🛰️ CLOUD (Reasoning & Synthesis)**: The **Warden (LLM/Gemini)** resides in the cloud. It receives "Semantic Facts" synthesized from local data and performs the high-level botanical reasoning, anomaly detection, and narrative generation.
- **🧠 THE BRIDGE: SILICA (Context Layer)**: A logic layer built on OpenClaw that prepares the **World Model** and **Semantic Synthesis** for the cloud-based Warden. It ensures the LLM receives high-value "Facts" rather than low-value "Noise."

---

## 2. THE WARDEN'S PROTOCOL (3-STEP LOOP)
The Warden executes a rigorous audit loop across the Local/Cloud boundary:

1.  **📊 STEP 1: COLLECT (Local / Python)**  
    OpenClaw executes local scripts on the MacBook to fetch raw telemetry, visual ground-truth, and micro-forecasts. Data is stored in `data/` and `media/`.
2.  **🔍 STEP 2: REASON (Cloud / LLM)**  
    Synthesized facts are sent to the cloud-based Warden. Using **SILICA Logic**, the Warden performs **Cross-Verification** (comparing $V_{gt}$ vs. $S_t$) and reconciles local observations with the World Model.
3.  **📢 STEP 3: SHARE (Public / GardenOS)**  
    The Warden's narrative is pushed to the public interface (Slack/Blog) via local synchronization (`sync.sh`).

---

## 3. DOMAIN SEPARATION
- **💻 LOCAL (Device)**: OpenClaw execution, Python collection on MacBook, and raw data storage (`data/`, `media/`).
- **☁️ CLOUD (Intelligence)**: The Warden's reasoning (Gemini API) and persistent state (GitHub Private Repository).
- **📢 PUBLIC (Presentation)**: GardenOS Website (Netlify) and Slack (#plantclaw).
