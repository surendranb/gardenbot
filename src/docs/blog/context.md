# 🧠 Gardenbot Value Optimization: Master Context Architecture

If token limits are removed as a constraint, the singular goal becomes **Maximizing Real-World Reasoning Fidelity**. An LLM is a stateless reasoning engine; it maps the text/image context it receives to an internal multidimensional space. To make it act as a highly capable "Curious Warden," we must perfectly structure its perception of the world. 

Here is the deep-thought restructuring of Gardenbot’s context delivery pipeline.

## 1. The Ontology of an Agent Prompt
A highly capable agent needs its input cleanly partitioned. Mixing instructions, identity, and data causes "attention dilution."

### **A. The System Prompt (The Agent's "Self")**
*What it is*: Identity, core operating philosophy, invariant rules, and output schema.
*For Gardenbot*:
- **Identity**: The Curious Warden (Tropical Agricultural Statistician).
- **Core Axioms**: "Visual turgidity proves hydration regardless of capacitive sensor output."
- **Directives**: Always execute the Flicker Test. Always identify one anomaly in the negative space.

### **B. The Context Payload (The "World State")**
*What it is*: The objective reality of the biome at the moment of execution.
*For Gardenbot*:
- **Static Reality**: The `GARDEN_MANIFEST.md` (Plant IDs, baseline geometries like the 50mm White Rabbit).
- **Temporal Reality**: The specific timeline of events.
- **Sensory Reality**: Cleanly formatted data arrays.

### **C. The User Prompt (The "Trigger")**
*What it is*: The specific mission for this exact invocation.
*For Gardenbot*: "Evaluate the current State Context against the 24-hour baseline image. Execute the Warden Protocol and update the ledger."

---

## 2. Restructuring the Data Modalities (No More Raw CSVs)
Raw CSVs are computationally "cheap" but semantically "poor" for LLMs. LLMs are next-token predictors trained on natural language; dumping raw tabular arrays forces the LLM to spend attention tokens spatially parsing commas.

### **The Shift to "Semantic State Summaries"**
Instead of `time,temp,hum\n10:00,31.2,18\n10:20,31.5,17`, the Python pre-processor (`prep_observer_context.py`) should handle the math and deliver a **Narrative State**:
```markdown
### 🌡️ Environment Vector
- **Temperature**: 31.5°C (Trending up +0.3°C/hr).
- **Humidity**: 17% (Persistently critical, desert-dry).
- **Soil Moisture**: p3 is at 71.2% (Dropping slowly, root zone is wet).
- **Weather Forecast**: Heat spike to 34°C expected at 14:00.
```
*Why this drives value*: The LLM no longer has to deduce the trend; it receives the trend as an explicit semantic fact. It can immediately dedicate its reasoning power to *what that trend means for the plant*.

## 3. Optimizing Visual Perception (Direct A/B Injection)
Currently, we tell the LLM: *"Compare current frame to the baseline from YESTERDAY (reference photos in archive/)."*
This is inefficient. It requires the LLM to search a directory, pick a file, and hold it. 

**The High-Value Restructure**:
We must spoon-feed the temporal visual delta. The pre-processing script (`prep_observer_context.py`) should explicitly locate yesterday's exact 24h photo and feed it directly into the prompt payload alongside `latest.jpg`.
- **Input Image 1**: `baseline_yesterday.jpg`
- **Input Image 2**: `latest_now.jpg`
*Why this drives value*: When an LLM vision model receives two images side-by-side explicitly labeled as "T-24h" and "T-0", its ability to detect object deltas (leaf growth, drooping, necrosis expansion) skyrockets. 

## 4. Episodic Memory (The Ledger)
The `vision_ledger.md` is currently appended sequentially. 
To maximize real-world value, the context payload should parse the ledger and present:
1. **The Last Verdict**: "You previously noted p3 tip burn and ordered misting."
2. **The Long-Term Anomaly Tracker**: "p4 has had a localized wilt for 4 straight days."
By structuring memory conceptually rather than chronologically, the agent maintains a continuous thread of investigation.

---

## 5. Concrete Restructuring Plan for Gardenbot V5
To implement this high-fidelity reasoning:

1. **Overhaul `prep_observer_context.py`**:
   - Make it compute trends (deltas) from the CSVs.
   - Make it output a clean `StateOfTheWorld.md` using semantic narrative language.
   - Make it automatically copy/symlink the exact 24-hour old photo to `docs/media/baseline_24h.jpg`.

2. **Refine `jobs.json`**:
   - Extract the heavy personality instructions into a true **System Prompt** (if OpenClaw supports an explicit system parameter, otherwise at the very top of the prompt).
   - Instruct the vision model to explicitly perform a side-by-side comparison of `docs/media/baseline_24h.jpg` and `docs/media/latest.jpg`.

This structure guarantees that every token spent is focused on higher-order botanical reasoning rather than low-level data extraction.
