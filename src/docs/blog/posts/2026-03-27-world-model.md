---
date: 2026-03-27
description: How SILICA grounds the LLM in physical reality and prevents hallucinated plant stress.
categories:
  - Context Engineering
---

# Building a Context Layer for the GardenBot

## The problem

Using an LLM to monitor 3 pots on my desktop is fun, but it kept guessing. Each cycle starts from scratch, and an LLM with no memory defaults to pattern-matching. It sees *"Chennai, 32°C, 60% humidity"* and concludes the plants must be wilting. Makes sense if you're going by vibes. Completely wrong physically.

<!-- more -->

The plants sit on a desk in an HVAC-clamped room. The AC holds temp at **26°C** and crushes humidity below **30%**. VPD regularly hits **3.5+ kPa** — that's extreme dryness, the opposite of what "tropical Chennai" would suggest. Without grounding, the LLM hallucinates stress symptoms that match the *outdoor* climate, not the actual microclimate 2 meters from a north-facing window.

## SILICA

SILICA is what I'm calling the context layer. It's not one script — it's a few things that sit between raw data and the LLM.

`prep_observer_context.py` is the main piece. It reads all the data files from the collection scripts (`warden.py`, `vision.py`, `weather_scout.py`), merges them with the world model and plant config, and outputs `observer_context.md`.

`GARDEN_MANIFEST.md` is the **world model**. I wrote it by hand — it codifies the physical constants of the desk biome. The north window gives only indirect light. The east wall blocks morning sun. The AC clamps temp at 26°C but tanks humidity. The terrace above radiates heat between noon and 3pm. These are things the LLM can't figure out from sensor readings alone.

`scripts/config/plants.json` has species info, sensor calibration, and dry thresholds for each pot.

The collection scripts run independently via cron/launchd. They write flat files. SILICA reads those files — it doesn't run them. OpenClaw doesn't run them either. **Data collection has no dependency on reasoning.**

## Why semantic synthesis matters

Raw CSV rows are bad LLM input. A row like `2026-03-27T14:30:00,27.1,28.2,412,wet,dry,wet` is meaningless without schema, calibration, and context. The model would need to know which column is which, what the thresholds are, what "wet" means for each species, and how the reading compares to recent trends.

`prep_observer_context.py` does that translation. It produces facts like:

- "Temperature: 27.1°C — within normal indoor range, AC active"
- "VPD: 3.5 kPa, rising trend — low humidity stress likely"
- "Soil p1 (Nickels): dry, below threshold — watering recommended"
- "Vision: Gemma 3 reports slight leaf curl on Pothos, consistent with low humidity"

The LLM gets `observer_context.md` — pre-digested facts — instead of CSVs. And because the world model is baked in, it knows "32°C outdoors" doesn't mean the plants are at 32°C.

## What changed

Before SILICA, the LLM would see Chennai weather and hallucinate heat stress. It'd recommend misting because it assumed tropical humidity, when the room is actually bone-dry from the AC. It flagged "high temperature" when the desk has never been above 28°C.

After SILICA, it flags the real problems — high VPD causing leaf curl, dry soil in specific pots, sensor readings that contradict what Gemma 3 sees in the image. Much more useful once I stopped letting it guess and started feeding it facts.

## What's next

Moving historical data into SQLite for faster trend queries. Hardening the launchd services so camera warmup happens reliably. Extending the reasoning window so the LLM has time for complex audits. But the foundation — grounding the model in a world model — that part works.
