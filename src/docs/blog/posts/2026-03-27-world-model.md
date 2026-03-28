---
date: 2026-03-27
description: How SILICA grounds the LLM in physical reality and prevents hallucinated plant stress.
categories:
  - Context Engineering
---

# Building a Context Layer for the GardenBot

## The problem

Using an LLM to monitor 3 pots on my desktop is a fun idea. But ultimately just dumping numbers into an LLM is no joy. 

Each cycle starts from scratch, and an LLM with no memory defaults to pattern-matching. It sees *"Chennai, 32°C, 60% humidity"* and concludes the plants must be wilting. Makes sense if you're going by vibes. It doesn't take into account the fact that the plants are indoors or how the room is aligned to the sun or what is the actual physics.

<!-- more -->

The plants sit on my desk. Once in a while I turn on the AC, which is also set to a max of **26°C**. If it is on it pushes humidity below **30%**. This makes the room dry and VPD regularly hits **3.5+ kPa**, the opposite of what "tropical Chennai" would suggest. Without grounding, the LLM hallucinates stress symptoms that match the *outdoor* climate, not the actual microclimate 2 meters from a north-facing window.

## SILICA

The answer: Build a context layer. SILICA is we named it. It is the abbreviation of "Semantic Intelligence & Local Indoor Context Awareness for Agentic Bio-Monitoring". A collection of scripts that sit between raw data and the LLM.

`prep_observer_context.py` does the heavy lifting. It reads all the data files from the collection scripts (`warden.py`, `vision.py`, `weather_scout.py`), merges them with the world model and plant config, and outputs `observer_context.md`.

`GARDEN_MANIFEST.md` is the **world model**. It codifies the physical constants of the desk biome. The north window gives only indirect light. The east wall blocks morning sun. The AC, if on, clamps temp at 26°C but tanks humidity. The terrace above radiates heat between noon and 3pm. These are things the LLM can't figure out from sensor readings alone.

`scripts/config/plants.json` has species info, sensor calibration, and dry thresholds for each pot.

The collection scripts run independently via cron/launchd. They write flat files. SILICA reads those files and prepares the context of the agent to pass on to the LLM.

The reason I use OpenClaw for this is - it makes the human in the loop easy/possible. When the agent finishes, it posts the observation and tells me what to do about it - water, mist etc. I reply in the thread once in a while about if I did act on its advice and it is added to the context layer in return.

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

Moving historical data into SQLite for faster trend queries. Hardening the launchd services so camera warmup happens reliably. Extending the reasoning window so the LLM has time for complex audits. All this would be building on top of the system that's grounded in a world model.
