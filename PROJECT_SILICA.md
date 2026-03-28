# SILICA: Cognitive Architecture for Botanical Intelligence
*Semantic Intelligence & Local Indoor Context Awareness for Agentic Bio-Monitoring*

## 1. Abstract
Bio-monitoring in extreme microclimates (e.g., an indoor desk in Chennai, India) presents a unique challenge for autonomous agents: the divergence between macro-weather forecasts and local indoor physics. Project SILICA proposes a "Context Layer" architecture that bridges raw sensor data with Large Language Model (LLM) reasoning through **Semantic Synthesis** and a persistent **World Model**. We examine the shift from stateless inference to stateful guardianship.

## 2. The Problem: Stateless Inference in a Stateful World
### 2.1 LLM Statelessness ($f(x) \to y$)
LLMs are essentially stateless functions. They do not possess a persistent internal state ($S_t$) that evolves across time steps. For a "Garden Warden" running every 3 hours, each invocation is a *Tabula Rasa*.
*   **The Problem**: Without explicit memory management, the AI cannot distinguish between a transient sensor spike and a degenerative trend (e.g., root rot).
*   **Example**: If the moisture drops at 12:00 PM, the 3:00 PM invocation "forgets" the event unless the agent injects it. To the AI, every 3 hours is "Day 1."

### 2.2 The Stochastic Hallucination & Physics Gap
LLMs lack visceral grounding in thermodynamics. They process `34°C` as a linguistic token rather than a thermal pressure.
*   **The Concept**: Stochastic Hallucination occurs when an AI prioritizes "Narrative Plausibility" over "Visual Ground-Truth."
*   **Example**: Seeing `High Temp` in the logs, the AI's training weights bias it toward reporting "wilting" in the image, even if the Mexican Mint's leaves are physically turgid. It hallucinates stress to satisfy its internal statistical model of "Heat + Plants."

## 3. The Solution: Agentic Control Loops & Memory
### 3.1 Agents as the "Pre-frontal Cortex"
While the LLM is the "Executive," the **Agent** is the system that manages the **Sense-Plan-Act** loop. The Agent provides the $S_t$ (State) that the LLM lacks.
*   **Example**: The Agent retrieves $S_{t-1}$ from a database (e.g., "Yesterday's 06:00 baseline") and presents it as a **Comparative Fact**. This transforms the AI from a "Data Reader" into a "Trend Analyst."

### 3.2 The Context Layer & Information Bottlenecks
Feeding raw numeric logs into a context window is an inefficient use of compute—it increases **Entropy**. 
*   **The Concept**: Information Bottleneck. We must maximize "Predictive Utility" while minimizing "Irrelevant Noise."
*   **The SILICA Fix**: We condense 100 raw telemetry rows into **Semantic Facts**. 
    *   *Raw*: `32.1, 32.2, 32.1...`
    *   *Semantic*: `State: Isothermal Stability (32°C). Variance: <1%.` This allows the LLM to reason at a higher level of abstraction (meta-reasoning).

## 4. Architectural Evolution: From Filesystem to Knowledge Graph
How we store context defines how the agent "thinks." We categorize the evolution of agentic memory into three tiers:

### 4.1 Tier 1: Filesystem-as-Context (Current)
*   **Mechanism**: Utilizing human-readable files (`GARDEN_MANIFEST.md`, `telemetry.csv`, `vision_ledger.md`).
*   **The Philosophy**: Git-traceable and observable. The filesystem is the "External Brain."
*   **The Limitation**: Linear retrieval. As logs grow, the agent's "Working Memory" (context window) becomes saturated with low-value tokens.

### 4.2 Tier 2: Relational Memory (The "Metrics Engine")
*   **Mechanism**: Migrating to structured databases (e.g., SQLite).
*   **The Philosophy**: Rapid retrieval of **Aggregates**. Instead of reading 100 lines, the agent queries: `SELECT avg(vpd) FROM metrics WHERE timestamp > now - 24h`.
*   **Impact**: Enables **Deterministic Baselining**. The agent knows "Normal" with mathematical precision before it ever starts reasoning.

### 4.3 Tier 3: Semantic Knowledge Graphs
*   **Mechanism**: Linking entities (Plant → Species → Physiology → Current Biome).
*   **The Philosophy**: Deductive Reasoning.
*   **Example**: "P1 is a *Dischidia* (Species). *Dischidias* are epiphytes (Physiology). Epiphytes prefer high humidity (Requirement). Current Biome is 30% (Conflict). **Deduction**: Increase misting frequency."

## 5. The SILICA World Model: Codifying the "Indoor Truth"
To bridge the "Atmospheric Paradox" (Indoor vs. Outdoor divergence), we codify the **Physical Laws of the Desk**:
*   **Lighting Geometry**: North-facing diffuse light + East-facing shielding.
    *   *Research Insight*: The AI learns that "Shadow Shift" is a proxy for time-of-day, even under constant LED fill-light.
*   **Atmospheric Shielding**: AC at 26°C provides a "Thermal Floor."
    *   *Example**: Even if Chennai is 40°C, the AI "knows" the plants are safe within their HVAC-clamped microclimate. 
*   **Occupancy Synergy**: Your 12-hour desk presence provides localized CO2 enrichment and thermal mass.

## 6. Conclusion: From Watching to Understanding
Project SILICA is not "Automation"—it is **Cognitive Extension**. By building a Context Layer and a persistent Memory Core, we provide the LLM with the one thing it lacks: **Experience**.  We are building an example of how AI can solve real-world problems by being a world-aware Observer that guides human action.

---

## PROJECT ROADMAP (The Checklist)

### Phase 1: Biome Reconstruction (The World Model) [/]
- [x] Biome Questionnaire & Data Gathering
- [x] Document World Model Constants in `GARDEN_MANIFEST.md`
- [/] Upgrade `prep_observer_context.py` for Semantic Fact Synthesis
- [ ] Verification: Test Warden response to "Indoor Truth"

### Phase 2: Narrative & Sharing [ ]
- [x] Deep Document: "SILICA: Cognitive Architecture for Botanical Intelligence"
- [ ] Write Blog Post: "Beyond the Baseline: Building a World Model"
- [ ] Update `PROJECT_MOAT.md` with Silica architecture

### Phase 3: Agentic Memory Core [ ]
- [ ] Design Schema for `memory.db` (SQLite)
- [ ] Implement "Anomaly Detection" baseline comparison
- [ ] Implement "Phenological Event" tracking (Growth, Leaf Count)

### Phase 4: Predictive Modeling [ ]
- [ ] Implement "Stress Foresight" (VPD slope prediction)
- [ ] Final Verification: 48-hour autonomous run with world-aware reasoning
