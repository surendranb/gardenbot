# 🏗️ GardenOS V4: Scalable Agent Architecture

To move from a "Scripted Observer" to a "True Botanical Agent," we must shift from **Data Injection** to **Semantic Reasoning**. Here is the architectural roadmap from an AI/ML Engineer's perspective.

## 1. The Epistemic Layer (Storage & Retrieval)
*Current: Flat CSV/Markdown logs.*
*V4: The Tri-Modal Memory System.*

- **Temporal Layer (SQL/TimescaleDB)**: For quantitative metrics. Enables the agent to query: *"What was the avg. VPD during my last 5 waterings?"*
- **Episodic Layer (Vector Store/RAG)**: For visual history and long-form analysis. Enables: *"Search photos from 6 months ago for similar leaf discoloration on p3."*
- **Ground Truth Layer (YAML/JSON)**: For static constants (The Manifest).

## 2. The Semantic Middleware (Context Transformation)
Instead of feeding raw CSVs to the LLM (which wastes tokens and causes 'Numeric Noise'), we implement a **Feature Extraction** layer before the prompt:

- **Signal vs. Noise**: Don't send `29.8, 29.9, 30.1`. Send `Trend: Warming (+0.3°C/hr) | State: Thermal Stress Imminent`.
- **Semantic Tags**: Tag every data point with its **Meaning**.
  - `hum: 18%` → `status: DESERT_DRY | impact: TRANSPIRATION_SHOCK_RISK`.
- **Ontology**: Define the **'Garden Event'**.
  - An **Event** = [Visual Delta] + [Sensor Delta] + [Weather Context] + [Actor Intervention].

## 3. The Botanical Ontology (Entity-Relationship)
We define the garden as a graph of entities:
- **`Pot`**: A physical container (The Biome).
- **`Plant`**: A biological entity inside a `Pot`.
- **`Sensor`**: A digital witness attached to a `Pot` or `Environment`.
- **`Constraint`**: The physical limits (The "Mission").

**The Value Flow**:
The agent doesn't "see" a JPEG. It sees a **Scene Graph**:
`[Pot p2] contains [Plant Mexican Mint] showing [New Stem Node] while [Sensor A5] reports [Moisture Descent].`

## 4. The Reasoning Loop (Agent Molt)
1. **Perception**: Extract semantic features from `latest.jpg` + CSV.
2. **Retrieval**: Query Vector DB: *"Has p2 ever shown node emergence this fast in >30°C weather?"*
3. **Synthesis**: Correlate Retrieval + Perception + Weather.
4. **Action**: The Warden's Decision (A deterministic instruction to the human).

## 5. Technical Stack Upgrade
- **Database**: SQLite (local) for metrics. Extremely portable and queryable.
- **RAG Engine**: ChromaDB or Qdrant (local) for visual memory and previous analysis logs.
- **Context Orchestrator**: A Python-based `ContextManager` class that assembles the prompt dynamically based on **Information Density** (if nothing changed, keep it short; if an anomaly is detected, pull deeply from history).

---

**Summary**: By moving to this architecture, we reduce the agent's **Cognitive Load** (less raw data parsing) and increase its **Situational Memory** (6 months vs 6 entries).
