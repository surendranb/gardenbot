#!/usr/bin/env python3
import base64
import json
import os
import sqlite3
import subprocess
import time
import sys
from datetime import datetime
from google import genai
from google.genai import types

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
DB_PATH = os.path.join(BASE_DIR, "data/garden.db")
PHOTO_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
ENV_PATH = os.path.join(BASE_DIR, ".env")
VISION_MODEL = "gemini-2.5-flash"

def load_env_file(path):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

def capture_image():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    day_dir = os.path.join(ARCHIVE_DIR, today_str)
    os.makedirs(day_dir, exist_ok=True)
    os.makedirs(os.path.dirname(PHOTO_PATH), exist_ok=True)
    
    ts = now.strftime("%H%M%S")
    archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")
    
    # Try OpenCV first
    try:
        import cv2
        import numpy as np
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Warmup for auto-exposure stabilization
        print("Vision: OpenCV Warmup...")
        for _ in range(15):
            cap.read()
            time.sleep(0.1)
            
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            cv2.imwrite(archive_path, frame)
            print(f"Vision: Image captured via OpenCV to {archive_path}")
        else:
            raise RuntimeError("OpenCV frame read failed")
    except Exception as e:
        print(f"OpenCV failed: {e}. Falling back to imagesnap...")
        try:
            subprocess.run(["/opt/homebrew/bin/imagesnap", "-w", "3", "-q", archive_path], check=True, timeout=20)
            print(f"Vision: Image captured via imagesnap to {archive_path}")
        except Exception as e2:
            print(f"Vision Capture Failed: {e2}")
            return None

    if os.path.exists(archive_path):
        # copy to latest.jpg
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True, timeout=5)
        return archive_path
    return None

def analyze_with_gemini(client, image_path, prev_leaf_count, prev_turgidity, prev_turgidity_score, prev_height, prev_width, baseline=False):
    if baseline:
        print("Vision: Establishing fresh baseline calibration with physical desk context...")
    else:
        print(f"Vision: Analyzing with Gemini (Prev Leaves: {prev_leaf_count}, Turgidity: {prev_turgidity_score}, Height: {prev_height}cm, Width: {prev_width}cm)...")
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        if baseline:
            prompt = (
                "You are the Garden Botanical Observer. Your task is to perform a deterministic physical audit to establish a fresh baseline calibration of a new Jade plant (Crassula ovata).\n\n"
                "PHYSICAL CALIBRATION CONTEXT:\n"
                "- The camera is a USB webcam mounted approximately 40 cm away from the plant at a 45-degree downward angle.\n"
                "- The pot has a circular rim with a physical diameter of exactly 8.0 cm.\n"
                "- There are two reference objects in the pot: a toy rabbit (right) and a soil sensor plunge (left). Both are exactly 5.0 cm tall.\n"
                "- The Jade plant has two stalks: a larger stalk on the left (physical baseline height: 8.0 cm) and a smaller stalk on the right (physical baseline height: 7.0 cm).\n\n"
                "INSTRUCTIONS:\n"
                "1. Count every single leaf visible in the image. Be extremely meticulous. Count rosettes and individual leaves.\n"
                "2. Set leaf_change to 0 (since this is the first baseline measurement).\n"
                "3. Set plant_height_cm to 8.0 (since the tallest stalk is physically measured at 8.0 cm for the baseline).\n"
                "4. Estimate canopy_width_cm (maximum horizontal spread of the plant canopy) using the 8.0 cm pot diameter and the 5.0 cm rabbit as horizontal scale guides.\n"
                "5. Grade visual turgidity_score on a scale of 0.0 to 1.0 based on leaf thickness, shininess, and plumpness. (1.0 is perfectly plump/hydrated, 0.0 is completely wilted. Below 0.7 is STRESSED, below 0.4 is WILTING).\n"
                "6. Classify turgidity: 'TURGID' (score >= 0.7), 'STRESSED' (score 0.4 - 0.7), or 'WILTING' (score < 0.4).\n"
                "7. Assess soil visual moisture state: 'DRY', 'MOIST', 'WET', or 'UNKNOWN'.\n\n"
                "Answer with a single JSON object. Make sure the JSON keys match exactly:\n"
                "{\n"
                '  "turgidity": "TURGID" or "STRESSED" or "WILTING",\n'
                '  "turgidity_score": 0.95,\n'
                '  "leaf_count": 34,\n'
                '  "leaf_change": 0,\n'
                '  "plant_height_cm": 8.0,\n'
                '  "canopy_width_cm": 10.5,\n'
                '  "soil_visual": "DRY" or "MOIST" or "WET" or "UNKNOWN",\n'
                '  "anomalies": "A short description of any visual leaf changes, color shifts, discolored spots, or new stems",\n'
                '  "confidence": 0.95\n'
                "}\n"
                "Return only the raw JSON. No markdown formatting, no code blocks."
            )
        else:
            prompt = (
                "You are the Garden Botanical Observer. Your task is to perform a deterministic physical audit of a Jade plant (Crassula ovata).\n\n"
                "PHYSICAL CALIBRATION CONTEXT:\n"
                "- The camera is a USB webcam mounted approximately 40 cm away from the plant at a 45-degree downward angle.\n"
                "- The pot has a circular rim with a physical diameter of exactly 8.0 cm.\n"
                "- There are two reference objects in the pot: a toy rabbit (right) and a soil sensor plunge (left). Both are exactly 5.0 cm tall.\n"
                "- The Jade plant has two stalks: a larger stalk on the left (physical baseline height: 8.0 cm) and a smaller stalk on the right (physical baseline height: 7.0 cm).\n\n"
                "To maintain temporal consistency, here is the previous state recorded:\n"
                f"- Previous Leaf Count: {prev_leaf_count} leaves\n"
                f"- Previous Turgidity Classification: {prev_turgidity}\n"
                f"- Previous Turgidity Score: {prev_turgidity_score} (1.0 is perfectly plump/hydrated, 0.0 is completely wilted)\n"
                f"- Previous Plant Height: {prev_height} cm\n"
                f"- Previous Canopy Width: {prev_width} cm\n\n"
                "INSTRUCTIONS:\n"
                "1. Count every single leaf visible in the image. Be meticulous. Count rosettes and individual leaves.\n"
                "2. Compare this to the previous count. Deduce leaf_change (current_count - previous_count).\n"
                "3. Estimate plant_height_cm by evaluating if the main stalks have grown above their baseline heights (8.0 cm and 7.0 cm) using the 5.0 cm rabbit and sensor as vertical guides.\n"
                "4. Estimate canopy_width_cm (maximum horizontal spread of the plant canopy) using the 8.0 cm pot diameter and the 5.0 cm rabbit as horizontal scale guides.\n"
                "5. Grade visual turgidity_score on a scale of 0.0 to 1.0 based on leaf thickness, shininess, and plumpness. (Below 0.7 is STRESSED, below 0.4 is WILTING).\n"
                "6. Classify turgidity: 'TURGID' (score >= 0.7), 'STRESSED' (score 0.4 - 0.7), or 'WILTING' (score < 0.4).\n"
                "7. Assess soil visual moisture state: 'DRY', 'MOIST', 'WET', or 'UNKNOWN'.\n\n"
                "Answer with a single JSON object. Make sure the JSON keys match exactly:\n"
                "{\n"
                '  "turgidity": "TURGID" or "STRESSED" or "WILTING",\n'
                '  "turgidity_score": 0.95,\n'
                '  "leaf_count": 34,\n'
                '  "leaf_change": 2,\n'
                '  "plant_height_cm": 8.2,\n'
                '  "canopy_width_cm": 10.5,\n'
                '  "soil_visual": "DRY" or "MOIST" or "WET" or "UNKNOWN",\n'
                '  "anomalies": "A short description of any visual leaf changes, color shifts, discolored spots, or new stems",\n'
                '  "confidence": 0.95\n'
                "}\n"
                "Return only the raw JSON. No markdown formatting, no code blocks."
            )
        
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        response = client.models.generate_content(
            model=VISION_MODEL,
            contents=[prompt, image_part],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        
        raw_text = response.text.strip()
        parsed = json.loads(raw_text)
        return parsed, raw_text
    except Exception as e:
        print(f"Vision: Gemini Analysis Failed: {e}")
        return None, str(e)

def main():
    load_env_file(ENV_PATH)
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Vision: Error - GOOGLE_API_KEY not found in environment.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    baseline = "--baseline" in sys.argv or "--calibrate" in sys.argv
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_path = capture_image()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if not image_path:
        # Log capture failure
        c.execute("""
        INSERT OR REPLACE INTO vision (timestamp, image_path, model, turgidity, soil_visual, anomalies, confidence, leaf_count, leaf_change, turgidity_score, plant_height_cm, canopy_width_cm, raw_json)
        VALUES (?, NULL, ?, 'CAPTURE_FAILED', 'UNKNOWN', 'Camera capture failed', 0.0, NULL, NULL, NULL, NULL, NULL, '{}')
        """, (now_str, VISION_MODEL))
        conn.commit()
        conn.close()
        print("Vision: Logged capture failure to database.")
        return
        
    # Query previous reading to maintain consistency
    try:
        c.execute("""
            SELECT leaf_count, turgidity, turgidity_score, plant_height_cm, canopy_width_cm 
            FROM vision 
            WHERE turgidity != 'CAPTURE_FAILED' AND turgidity != 'ANALYSIS_FAILED' 
            ORDER BY timestamp DESC LIMIT 1
        """)
        last_vision = c.fetchone()
        prev_leaf_count = last_vision[0] if last_vision and last_vision[0] is not None else 32
        prev_turgidity = last_vision[1] if last_vision else "TURGID"
        prev_turgidity_score = last_vision[2] if last_vision and last_vision[2] is not None else 0.90
        prev_height = last_vision[3] if last_vision and last_vision[3] is not None else 10.0
        prev_width = last_vision[4] if last_vision and last_vision[4] is not None else 12.0
    except Exception:
        prev_leaf_count = 32
        prev_turgidity = "TURGID"
        prev_turgidity_score = 0.90
        prev_height = 10.0
        prev_width = 12.0
        
    analysis, raw_json = analyze_with_gemini(client, image_path, prev_leaf_count, prev_turgidity, prev_turgidity_score, prev_height, prev_width, baseline=baseline)
    
    if analysis:
        turgidity = analysis.get("turgidity", "UNKNOWN")
        soil_visual = analysis.get("soil_visual", "UNKNOWN")
        anomalies = analysis.get("anomalies", "")
        confidence = float(analysis.get("confidence", 1.0))
        leaf_count = int(analysis.get("leaf_count", prev_leaf_count))
        leaf_change = int(analysis.get("leaf_change", 0))
        turgidity_score = float(analysis.get("turgidity_score", prev_turgidity_score))
        val_height = analysis.get("plant_height_cm")
        plant_height_cm = float(val_height) if val_height is not None else None
        
        val_width = analysis.get("canopy_width_cm")
        canopy_width_cm = float(val_width) if val_width is not None else None
        
        c.execute("""
        INSERT OR REPLACE INTO vision (timestamp, image_path, model, turgidity, soil_visual, anomalies, confidence, leaf_count, leaf_change, turgidity_score, plant_height_cm, canopy_width_cm, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (now_str, image_path, VISION_MODEL, turgidity, soil_visual, anomalies, confidence, leaf_count, leaf_change, turgidity_score, plant_height_cm, canopy_width_cm, raw_json))
        print(f"Vision: Analysis logged (Turgidity: {turgidity} ({turgidity_score}), Leaves: {leaf_count} ({leaf_change}), Height: {plant_height_cm}cm, Width: {canopy_width_cm}cm)")
    else:
        # Analysis failed
        c.execute("""
        INSERT OR REPLACE INTO vision (timestamp, image_path, model, turgidity, soil_visual, anomalies, confidence, leaf_count, leaf_change, turgidity_score, plant_height_cm, canopy_width_cm, raw_json)
        VALUES (?, ?, ?, 'ANALYSIS_FAILED', 'UNKNOWN', ?, 0.0, NULL, NULL, NULL, NULL, NULL, ?)
        """, (now_str, image_path, VISION_MODEL, f"Gemini call failed: {raw_json}", raw_json))
        print("Vision: Logged analysis failure to database.")
        
    conn.commit()
    conn.close()


    
    # Trigger git push and static build sync.sh
    try:
        import subprocess
        subprocess.Popen(["/bin/bash", "/Users/surendran/.openclaw/workspace/gardenbot/scripts/sync.sh"])
        print("Vision: Dispatched sync.sh background process.")
    except Exception as e:
        print(f"Vision: Failed to dispatch sync.sh: {e}")

if __name__ == "__main__":
    main()

