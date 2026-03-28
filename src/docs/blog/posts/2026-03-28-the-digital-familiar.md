---
date: 2026-03-28
description: Transitioning GardenOS from a zero-trust observer to a context-aware system that cross-verifies sensors and vision.
categories:
  - Context Engineering
  - SILICA
draft: true
---

# From Data to Deduction

Last post I talked about SILICA — the context layer that grounds the Warden in the physical reality of the desk. Since then I've made a few changes that shifted how the system actually thinks.

## Cross-verification

For the first week, the protocol was simple: *visuals supersede sensors*. If the camera says the plant looks fine but the soil sensor says dry, trust the camera. A zero-trust approach to handle noisy capacitive probes.

That's not great long-term. The interesting signal is where the two **disagree**. So now the Warden compares sensor readings against visual evidence and flags divergences. If the soil reads 10% but the leaves are turgid and upright, it notes the mismatch and investigates. Could be sensor drift, could be recent watering that hasn't registered yet. Flagging the gap is more useful than ignoring one input.

<!-- more -->

## The human-gated microclimate

The biggest improvement was teaching the Warden about the cooling hierarchy. The biome isn't a lab — it's my desk, and the climate changes based on what I'm doing.

**Fan S** is always on when I'm sitting here. **Fan N** kicks in when it's hot. **The AC** is a last resort. Each step changes the environment differently — Fan S alone gives high air exchange that forces plants to transpire faster, which means VPD goes up. The AC crashes humidity entirely.

By encoding this in the world model, the Warden now understands that dry air isn't random — it's a predictable consequence of Fan S running while I'm at the desk. It treats **human presence as a climate variable**, not background noise.

## Better context synthesis

I updated `prep_observer_context.py` to produce higher-level facts. Instead of just reporting sensor values, it now infers state:

- "AC active — expect humidity drop and VPD spike, watch p1 for stress"
- "Human presence high — Fan S scouring leaf boundary layers"
- "Thermal peak from terrace ceiling, 12:00-15:00 window"

The Warden gets these as pre-built observations instead of having to piece together what's happening from raw numbers.

## Local-first, cloud-reasoning

The data stays on the MacBook. Collection scripts run via cron/launchd, write flat files, and don't touch the internet. The only cloud dependency is the LLM call during reasoning — and if that fails, everything else keeps logging. Secrets are in env vars, not config files.

I'm not just logging data anymore. The system knows the difference between a hot day in Chennai and a thirsty plant on a wooden desk. That's the part that took the most work to get right.
