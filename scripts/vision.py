#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import time
import json

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
PHOTO_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
DAILY_BENCHMARK_PATH = os.path.join(ARCHIVE_DIR, "daily_benchmark.jpg")

# Ensure directories exist
os.makedirs(os.path.dirname(PHOTO_PATH), exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

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
        print("Attempting camera capture using OpenCV (cv2)...")
        camera_index = 0
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {camera_index}")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Warmup (3 frames)
        print("Warming up sensor...")
        for i in range(3): 
            ret, frame = cap.read()
            if ret:
                print(f"  Warmup frame {i+1} captured.")
            time.sleep(0.5)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Failed to capture image from camera.")
        
        success = cv2.imwrite(archive_path, frame)
        if not success:
            raise RuntimeError(f"Failed to write image to {archive_path}")
        
        print(f"Image captured using CV2 and saved to {archive_path}")

    except Exception as e:
        print(f"CV2 failed or not available: {e}. Attempting imagesnap fallback...")
        try:
            subprocess.run(["imagesnap", "-q", archive_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Image captured using imagesnap and saved to {archive_path}")
        except Exception as e2:
            print(f"Vision failed completely: {e2}")
            return {"error": str(e2)}

    # Post-capture operations
    if os.path.exists(archive_path):
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
        print(f"Updated latest photo: {PHOTO_PATH}")
        
        # Handle daily benchmark at 6 AM
        if now.hour == 6 and now.minute < 15:
            subprocess.run(["cp", archive_path, DAILY_BENCHMARK_PATH], check=True)
            print(f"Updated Daily Benchmark: {DAILY_BENCHMARK_PATH}")

        return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
    else:
        return {"error": "Archive path does not exist after capture attempts."}

if __name__ == "__main__":
    res = capture_vision()
    print(json.dumps(res, indent=2))
