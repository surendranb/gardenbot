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
VISION_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-3.1-flash-lite-preview")
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
    """Captures an image, preferring cv2, falling back to imagesnap."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    day_dir = os.path.join(ARCHIVE_DIR, today_str)
    os.makedirs(day_dir, exist_ok=True)
    ts = now.strftime("%H%M%S")
    archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")

    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): raise RuntimeError("Cannot open camera")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for _ in range(3): cap.read(); time.sleep(0.5) # Warmup
        ret, frame = cap.read()
        cap.release()
        if not ret: raise RuntimeError("Capture failed")
        cv2.imwrite(archive_path, frame)
    except Exception as e:
        print(f"CV2 failed: {e}. Fallback to imagesnap...")
        try:
            subprocess.run(["imagesnap", "-q", archive_path], check=True)
        except Exception as e2:
            print(f"Vision failed: {e2}")
            return {"error": str(e2)}

    if os.path.exists(archive_path):
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
        if now.hour == 6 and now.minute < 15:
            subprocess.run(["cp", archive_path, DAILY_BENCHMARK_PATH], check=True)
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

def build_prompt():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"Today's Date: {now_str}\n"
        "You are the Garden Botanical Observer (Expert Visual Ethologist).\n"
        "Your task is to perform a meticulous physical audit and EXPLANATORY health inference of a CHRONOLOGICAL sequence of images. Starting from the oldest to the newsest (now)\n"
        "Create a detailed checklist of each plant"
        "You will follow a maker-checker mechanism. Describe what you will do first and then validate after you've done your interpretation. You job is to interpret the images accurately with a keen eye and the expeience of a renowned botanist"
        "You will audit each image carefully from oldest to newest & ask after each image, what changed. Then write a detailed note about that"
        "Return one strict JSON object and nothing else.\n\n"
        "WORLD MODEL:\n"
        "- Plants are indoor on the desk."
        "- LIGHTING: Fixed Camera LED (cool spectrum) + Diffuse light from a North window. ZERO direct sunlight.\n"
        "- SCALE ANCHOR: White rabbit (5cm) in p3 pot.\n"
        "- ORIENTATION (Calibration):\n"
        "  * p1 (String of Nickels, Yellow pot): Has many leaves.\n"
        "  * p2 (Mexican Mint) (Black pot): In the center of the pot. Has two big wide leaves and pair of smaller ones coming up. \n\n"
        "  * p3 (Pothos, Black pot): Has 2 leaves and a rabbit toy for reference.\n"
        "  * p4 (Silver Guest) (Black pot): Smallest and near the rim of the pot. Shares the pot with mexican mint.\n\n"
        "IMAGE LABELS:\n"
        "- Sequence shows images taken during midday from last 5 days + Today's morning 'Rested State' + CURRENT.\n\n"
        "BIOME-WIDE MONITORING (The 'Beyond-Inventory' Rule):\n"
        "- Your audit must include the ENTIRE pot surface. \n"
        "- Identify 'Incidental Growth': Note any weeds, moss, secondary seedlings, or uncatalogued sprouts in the soil of p1-p4.\n"
        "- Identify 'Biome Anomalies': Note changes in soil texture (cracking vs. dampness), fungal presence, or debris on the desk surface.\n\n"
        "REQUIRED AUDIT FOR EACH PLANT (p1-p4) & THE BIOME:\n"
        "FOR EACH PLANT (p1-p4), PROVIDE AN EXPLANATORY AUDIT. DO NOT MIX UP THE PLANT NAMES OR ORDER & DOUBLE CHECK :\n"
        "1. PHYSICAL FACTS: Leaf count, specific color gradients, and exact posture relative to pot rims.\n"
        "2. EXPLANATORY TRANSFORMATIONS: Do not just state change; explain the trajectory. (e.g., 'Compared to Yesterday mid-day, the apical leaf on p3 has dropped by 5mm, whereas 3 days ago it was level with the pot rim').\n"
        "3. PIXEL-BASED HEALTH REASONING: Deduce health using VISUAL EVIDENCE ONLY. If you say 'stressed', you must cite the specific visual evidence (e.g., 'Reasoning: p2 is exhibiting leaf-margin necrosis that has progressed 2mm deeper since the 48h baseline').\n\n"
        "Output format (JSON keys):\n"
        "timestamp, model, plant_audit, biome_observations, temporal_deltas, visual_health_inference, anomalies, narrative_description, confidence.\n"
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
    
    # Bundle the prompt and the images
    contents = [build_prompt()]
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