#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
MEDIA_DIR = os.path.join(BASE_DIR, "media")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
PHOTO_PATH = os.path.join(MEDIA_DIR, "latest.jpg")
CAM_NAME = "USB2.0 PC CAMERA"

def capture_vision():
    try:
        import cv2
        camera_index = 0
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened(): raise RuntimeError(f"Cannot open camera {camera_index}")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for _ in range(5): cap.read()
        ret, frame = cap.read()
        cap.release()
        if not ret: raise RuntimeError("Failed to capture image from camera")
        
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = os.path.join(ARCHIVE_DIR, today)
        os.makedirs(day_dir, exist_ok=True)
        ts = datetime.now().strftime("%H%M%S")
        archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")
        cv2.imwrite(archive_path, frame)
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
        return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
    except Exception as e:
        # Fallback to imagesnap
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            day_dir = os.path.join(ARCHIVE_DIR, today)
            os.makedirs(day_dir, exist_ok=True)
            ts = datetime.now().strftime("%H%M%S")
            archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")
            subprocess.run(["imagesnap", "-d", CAM_NAME, "-q", archive_path], check=True)
            subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
            return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
        except Exception as e2:
            return {"error": f"Vision failed: {str(e2)}"}

if __name__ == "__main__":
    import json
    print(json.dumps(capture_vision(), indent=2))