#!/usr/bin/env python3
import base64
import requests
import json
import os
import sys
from datetime import datetime

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

MANIFEST_PATH = os.path.join(BASE_DIR, "GARDEN_MANIFEST.md")
CONTEXT_PATH = os.path.join(BASE_DIR, "data/observer_context.md")
IMAGE_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
LEDGER_PATH = os.path.join(BASE_DIR, "logs/vision_ledger.md")
SLACK_FALLBACK = os.path.join(BASE_DIR, "logs/slack_fallback.md")

# Models
VISION_MODEL = "google/gemma-3-12b-it:free"
REASONING_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_openrouter(model_id, prompt, image_base64=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "GardenWarden-Silica"
    }
    
    content = [{"type": "text", "text": prompt}]
    if image_base64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })
        
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": content}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    if response.status_code != 200:
        raise Exception(f"OpenRouter Error: {response.text}")
    return response.json()['choices'][0]['message']['content']

def main():
    print(f"[{datetime.now().isoformat()}] Starting SILICA Orchestrator...")
    
    # 1. Load Context
    with open(MANIFEST_PATH, 'r') as f: manifest = f.read()
    with open(CONTEXT_PATH, 'r') as f: context = f.read()
    
    # 2. Vision Interpretation (The Eyes)
    print(f"Calling Vision Layer ({VISION_MODEL})...")
    img_b64 = encode_image(IMAGE_PATH)
    vision_prompt = "Analyze this garden image. Identify specific non-plant objects, soil moisture appearance, and plant turgidity details."
    vision_description = call_openrouter(VISION_MODEL, vision_prompt, img_b64)
    print(f"Vision Result: {vision_description[:100]}...")

    # 3. Final Reasoning (The Brain)
    print(f"Calling Reasoning Layer ({REASONING_MODEL})...")
    reasoning_prompt = f"""
You are the Garden Warden—an expert agricultural statistician. 
MISSION: Conduct a ZERO-TRUST AUDIT using the provided 'Indoor Truth'.

**WORLD MODEL & CONTEXT:**
{manifest}

**TELEMETRY & SEMANTIC FACTS:**
{context}

**VISUAL INTERPRETATION (PROVIDED BY EYES):**
{vision_description}

**TASKS:**
1. Deduce plant health by correlating the 'Indoor Truth' (AC/Light) vs Visuals vs Sensors.
2. Identify anomalies.

**OUTPUT FORMAT (MANDATORY):**
- **Vitality Pulse**: p1-p4 Status.
- **The Biome Discovery**: Non-plant observations from Eyes.
- **Growth Momentum**: Apical leans and stasis points.
- **Weather Alignment**: Compare Indoor Truth vs Macro-forecast.
- **The Warden's Decision**: Verdict and Action.

Be concise. Use Meticulous tone.
"""
    final_report = call_openrouter(REASONING_MODEL, reasoning_prompt)
    
    # 4. Log and Report
    report_header = f"## WARDEN REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    full_entry = f"\n\n{report_header}\n{final_report}"
    
    with open(LEDGER_PATH, 'a') as f:
        f.write(full_entry)
    
    print("Report written to ledger.")
    
    # Slack fallback or direct send (simulated)
    # Note: For actual Slack send, we'd need a token, but here we append to fallback for visibility.
    with open(SLACK_FALLBACK, 'a') as f:
        f.write(full_entry)
    
    print("SILICA Run Complete.")

if __name__ == "__main__":
    main()
