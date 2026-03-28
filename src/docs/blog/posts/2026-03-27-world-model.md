---
date: 2026-03-27
description: How SILICA grounds the LLM in physical reality and prevents hallucinated plant stress.
categories:
  - Context Engineering
---

# Building a Context Layer for the GardenBot

## The Problem: LLMs Guess Based on Vibes

Using an LLM to monitor the 3 pots on my desktop is fun, but we ran into a problem fast — the model kept guessing. Each monitoring cycle starts from scratch, and an LLM with no memory defaults to "Predictive Guessing." It sees "Chennai, 32°C, 60% humidity" and concludes the plants must be wilting. Makes sense statistically. Completely wrong physically.

<!-- more -->

The plants sit on a desk inside an HVAC-clamped room. The AC holds temperature at 26°C and crushes humidity below 30%. The VPD regularly hits 3.5+ kPa — that's extreme dryness, the opposite of what "tropical Chennai" suggests. Without grounding, the LLM hallucinates stress symptoms that match the *outdoor* climate, not the actual microclimate 2 meters from a north-facing window.

## The Fix: SILICA

SILICA is what I'm calling the context layer. It's not one script or one service — it's a collection of things that sit between raw data collection and LLM reasoning.

The pieces:

- **`prep_observer_context.py`** — the synthesizer. It reads all the data files produced by the collection scripts (`warden.py`, `vision.py`, `weather_scout.py`), merges them with the World Model and plant config, and outputs a single `observer_context.md`.
- **`GARDEN_MANIFEST.md`** — the World Model. This is a document I wrote by hand that codifies the physical constants of the desk biome: the north-facing window provides only indirect diffuse light, the east wall blocks morning sun, the AC clamps temperature at 26°C but tanks humidity, the terrace above acts as a solar battery between noon and 3pm. These are things the LLM can't infer from sensor readings alone.
- **`scripts/config/plants.json`** — species metadata, sensor calibration, and dry thresholds for each pot.

The collection scripts (`warden.py`, `vision.py`, `weather_scout.py`) run independently at the OS level via cron/launchd. They write flat files to `data/`. SILICA reads those files — it doesn't run them. OpenClaw doesn't run them either. The data collection layer has no dependency on the reasoning layer.

## Semantic Synthesis: Why It Matters

The core idea is that raw CSV rows are bad input for an LLM. A row like `2026-03-27T14:30:00,27.1,28.2,412,wet,dry,wet` means nothing without schema, calibration, and context. The LLM would need to know which column is which, what the thresholds are, what "wet" vs "dry" means for each plant species, and how the current reading compares to recent trends.

`prep_observer_context.py` does this translation. It reads the raw data and produces semantic facts:

- "Temperature: 27.1°C — within normal indoor range, AC active"
- "VPD: EXTREME at 3.5 kPa, rising trend — low humidity stress likely"
- "Soil Moisture p1 (Nickels): DRY, below threshold — watering recommended"
- "Vision: Gemma 3 reports slight leaf curl on Pothos, consistent with low humidity"

The LLM receives `observer_context.md` — a document full of these pre-digested facts — instead of a pile of CSVs. It reasons at a higher semantic level, and because the World Model is baked in, it knows that "32°C outdoor temp" doesn't mean the plants are at 32°C.

## What This Actually Solved

Before SILICA, the LLM would see outdoor Chennai weather and hallucinate heat stress. It would recommend "misting" because it assumed tropical humidity, when in reality the room is bone-dry from the AC. It would flag "high temperature" when the desk has never been above 28°C.

After SILICA, the LLM knows the indoor microclimate is decoupled from outdoors. It flags the *actual* problems — high VPD causing leaf curl, dry soil in specific pots, or a sensor reading that contradicts what Gemma 3 sees in the image. The reasoning got dramatically more useful once we stopped letting the model guess and started feeding it facts.

## What's Next

The system works, but there's more to do. Moving the historical data into SQLite for sub-second trend queries. Hardening the launchd services so camera warmup happens reliably. And extending the reasoning window so the LLM has enough time to process complex multi-image audits without timing out. But the foundation — grounding the LLM in a deterministic World Model — that part is solid.
