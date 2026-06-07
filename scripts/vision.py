#!/usr/bin/env python3
import base64
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
PHOTO_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
VISION_JSON_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")
VISION_HISTORY_PATH = os.path.join(BASE_DIR, "logs/vision_history.jsonl")
DAILY_BENCHMARK_PATH = os.path.join(ARCHIVE_DIR, "daily_benchmark.jpg")
VISION_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-flash-latest")
VISION_CONTEXT_PATH = os.path.join(BASE_DIR, "data/vision_context.json")
ENV_PATH = os.path.join(BASE_DIR, ".env")

REFERENCE = {
    "rabbit_height_cm": 5.0,
    "camera_distance_cm": 30.0,
    "black_pot_diameter_cm": 12.0,
    "yellow_pot_diameter_cm": 10.0,
}

def load_env_file(path):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

def ensure_paths():
    os.makedirs(os.path.dirname(PHOTO_PATH), exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(VISION_JSON_PATH), exist_ok=True)

def capture_vision():
    """Captures an image, with adaptive exposure for night vision."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    day_dir = os.path.join(ARCHIVE_DIR, today_str)
    os.makedirs(day_dir, exist_ok=True)
    ts = now.strftime("%H%M%S")
    archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")

    try:
        import cv2
        import numpy as np
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): raise RuntimeError("Cannot open camera")
        
        # Hardware Tuning: Set resolution and suppress high-speed mode
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # --- ISP WARMUP & AUTO-EXPOSURE LOCK (SILICA v3.5) ---
        # We discard 20 frames to give the camera's AE/AWB time to stabilize 
        # specifically for night shots where the LED is the only source.
        print("Vision: Camera Warmup (AE/AWB Stabilization)...")
        for i in range(20):
            ret, _ = cap.read()
            if i % 10 == 0: time.sleep(0.2)
            
        ret, frame = cap.read()
        
        # --- BRIGHTNESS VALIDATION ---
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            print(f"Vision: Mean Pixel Intensity: {mean_brightness:.2f}")
            
            # If image is extremely dark (e.g. < 5.0), AE failed to ramp up.
            if mean_brightness < 5.0:
                print("Vision: WARNING: Frame underexposed. Attempting Recovery Capture...")
                time.sleep(2.0)
                # Second attempt with more settle time
                for _ in range(10): cap.read()
                ret, frame = cap.read()
        
        cap.release()
        if not ret: raise RuntimeError("Capture failed")
        cv2.imwrite(archive_path, frame)
        
    except Exception as e:
        print(f"CV2 failed: {e}. Fallback to imagesnap...")
        try:
            # Fallback to imagesnap with a longer warmup delay if possible
            subprocess.run(["imagesnap", "-w", "3", "-q", archive_path], check=True, timeout=20)
        except Exception as e2:
            print(f"Vision failed: {e2}")
            return {"error": str(e2)}

    if os.path.exists(archive_path):
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True, timeout=5)
        if now.hour == 6 and now.minute < 15:
            subprocess.run(["cp", archive_path, DAILY_BENCHMARK_PATH], check=True, timeout=5)
        return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
    return {"error": "Archive failed"}

def pick_temporal_stack(archive_path):
    """Multi-day sampling: Last 5 days' Peak Stress (12-2PM) + Today's First + CURRENT."""
    now = datetime.now()
    all_dates = sorted([d for d in os.listdir(ARCHIVE_DIR) if d.startswith("202")])
    target_dates = all_dates[-5:]
    
    stack = []
    for date_str in target_dates:
        day_dir = os.path.join(ARCHIVE_DIR, date_str)
        day_files = sorted([f for f in os.listdir(day_dir) if f.endswith(".jpg")])
        if not day_files: continue
        
        if date_str == now.strftime("%Y-%m-%d"):
            stack.append(os.path.join(day_dir, day_files[0])) # Today's Rested State

        peak_files = [f for f in day_files if 12 <= int(f.split('_')[1][:2]) <= 14]
        if peak_files:
            best_peak = min(peak_files, key=lambda x: abs(int(x.split('_')[1][:2]) - 13))
            path = os.path.join(day_dir, best_peak)
            if path not in stack: stack.append(path)

    if archive_path not in stack: stack.append(archive_path)
    
    return {
        "compare_set": stack,
        "current": archive_path,
        "anchor": stack[0] if stack else None,
        "previous": stack[-2] if len(stack) >= 2 else None
    }

def build_prompt(ctx=None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Load actual biome registry
    plants_config = []
    plants_json_path = os.path.join(BASE_DIR, "scripts/config/plants.json")
    if os.path.exists(plants_json_path):
        with open(plants_json_path, 'r') as f:
            plants_config = json.load(f)
    
    registry_str = ""
    for p in plants_config:
        registry_str += f"  * {p['id'].upper()}: {p['name']} ({p.get('species', 'Unknown')}) | Sensor: {p.get('sensor_key', 'None')}\n"
    if not registry_str:
        registry_str = "  * No plants currently registered."

    context_str = ""
    if ctx:
        actions = ctx.get("recent_human_actions", [])
        if actions:
            context_str += "\nRECENT HUMAN ACTIONS (A PRIORI KNOWLEDGE):\n"
            for a in actions:
                context_str += f"- {a.get('timestamp')}: {a.get('action')} - {a.get('note')}\n"
        
        if context_str:
            context_str += "\nCRITICAL INSTRUCTION: If you see visual changes that align with the human actions listed above, do NOT flag them as physiological stress. Instead, confirm their presence as successful outcomes of user care.\n"

    return (
        f"Today's Date: {now_str}\n"
        "You are the Garden Botanical Observer (Expert Visual Ethologist).\n"
        f"{context_str}"
        "Your task is to perform a meticulous physical audit and health inference of a CHRONOLOGICAL sequence of images. Starting from the oldest to the newest (now).\n"
        "You will follow a maker-checker mechanism. Describe what you will do first and then validate after you've done your interpretation.\n"
        "Return one strict JSON object and nothing else.\n\n"
        "WORLD MODEL:\n"
        "- Plants are indoor on the desk.\n"
        "- LIGHTING: Fixed Camera LED + Diffuse light from a North window. ZERO direct sunlight.\n"
        "- EXPECTED BIOME REGISTRY (A Priori):\n"
        f"{registry_str}\n"
        "- COMPOSITIONAL AUDIT REQUIREMENT:\n"
        "  * YOUR PRIMARY DIRECTIVE: Do not let the registry above blind you to physical reality. Use it as a 'Baseline Checklist' only.\n"
        "  * RECONCILIATION: Compare the current image against the registry. If a registered plant is missing, declare it a 'Systemic Loss'.\n"
        "  * ANOMALY DETECTION: If you see a leaf type, specimen, or structural change not in the registry, declare it a 'New Introduction/Intervention'.\n\n"
        "IMAGE LABELS:\n"
        "- Sequence shows images taken during midday from last 5 days + Today's morning 'Rested State' + CURRENT.\n\n"
        "REQUIRED AUDIT:\n"
        "1. Compositional Truth Check: List all pots and reconcile them against the registry.\n"
        "2. Multi-Day Comparative Audit: Describe how each occupant has transformed.\n"
        "3. Pixel-Based Health Reasoning: Deduce health using VISUAL EVIDENCE ONLY.\n\n"
        "Output format (JSON keys):\n"
        "timestamp, compositional_truth_check, inventory_reconciliation, plant_audit, biome_observations, visual_health_inference, anomalies, narrative_description, confidence.\n"
        "The JSON must be parseable. No markdown fences."
    )

def extract_json_payload(text):
    cleaned = text.strip().replace("```json", "").replace("```", "").strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        try: return json.loads(cleaned[start:end+1])
        except: pass
    raise ValueError("No valid JSON")

def main():
    load_env_file(ENV_PATH)
    ensure_paths()
    res = capture_vision()
    if "error" in res:
        print(f"Capture error: {res['error']}")
        return
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment.")
        return
        
    client = genai.Client(api_key=api_key)
    stack_info = pick_temporal_stack(res["archive_path"])
    
    # Load context if available
    ctx = None
    if os.path.exists(VISION_CONTEXT_PATH):
        try:
            with open(VISION_CONTEXT_PATH, 'r') as f:
                ctx = json.load(f)
            print(f"Vision: Loaded local context from {VISION_CONTEXT_PATH}")
        except Exception as e:
            print(f"Vision: Failed to load context: {e}")

    # Bundle the prompt and the images
    contents = [build_prompt(ctx)]
    frame_labels = []
    
    print(f"Vision: Sending {len(stack_info['compare_set'])} images to {VISION_MODEL}...")
    
    for i, path in enumerate(stack_info["compare_set"]):
        label = "EARLIEST" if i == 0 else "CURRENT" if i == len(stack_info["compare_set"])-1 else f"T-{len(stack_info['compare_set'])-1-i}"
        frame_labels.append({"label": label, "path": path})
        
        # Add label as text part
        contents.append(f"Image [{label}]:")
        
        # Add image data as bytes part
        try:
            with open(path, "rb") as f:
                image_data = f.read()
                contents.append(types.Part.from_bytes(data=image_data, mime_type="image/jpeg"))
            print(f"  Added {label}: {path}")
        except Exception as e:
            print(f"  Failed to add {label} ({path}): {e}")

    try:
        response = client.models.generate_content(
            model=VISION_MODEL, 
            contents=contents, 
            config=types.GenerateContentConfig(temperature=0.2)
        )
        
        # If the response is empty or blocked, handle it
        if not response.text:
            print("Vision: Received empty response from model.")
            return

        parsed = extract_json_payload(response.text)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "model": VISION_MODEL,
            "image_availability": stack_info,
            "frame_sequence": frame_labels,
            "vision_report": parsed
        }
        with open(VISION_JSON_PATH, "w") as f:
            json.dump(payload, f, indent=2)
        
        # Append to historical log
        with open(VISION_HISTORY_PATH, "a") as f:
            f.write(json.dumps(payload) + "\n")
            
        print(f"Vision JSON saved to {VISION_JSON_PATH} and history appended to {VISION_HISTORY_PATH}")
    except Exception as e:
        print(f"Inference failed: {e}")
        # If it failed, we might want to see the raw response for debugging
        try:
            if 'response' in locals() and response:
                print(f"Raw response text start: {response.text[:200]}...")
        except: pass

if __name__ == "__main__":
    main()