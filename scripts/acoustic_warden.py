#!/usr/bin/env python3
import subprocess
import re
import os
import sys

# --- Configuration ---
# Based on ffmpeg -list_devices, USB2.0 MIC is index 2
MIC_INDEX = "2"
DURATION = 5 # seconds
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
AUDIO_TMP = os.path.join(BASE_DIR, "logs/acoustic_test.wav")

def capture_volume():
    """Captures audio and returns the mean volume in dB."""
    print(f"Listening to the room for {DURATION} seconds...")
    
    # ffmpeg command to record and analyze volume statistics
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "avfoundation",
        "-i", f":{MIC_INDEX}",
        "-t", str(DURATION),
        "-filter:a", "volumedetect",
        "-f", "null",
        "/dev/null"
    ]
    
    try:
        # Run command and capture stderr where volumedetect outputs its data
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        output = result.stderr
        
        # Look for mean_volume in the output
        match = re.search(r"mean_volume: ([\-\d.]+) dB", output)
        if match:
            return float(match.group(1))
        else:
            print("Error: Could not find mean_volume in ffmpeg output.")
            print(output)
            return None
            
    except Exception as e:
        print(f"Acoustic Capture Failed: {e}")
        return None

if __name__ == "__main__":
    volume = capture_volume()
    if volume is not None:
        print(f"\n--- ACOUSTIC RESULT ---")
        print(f"Mean Volume: {volume} dB")
        print("-----------------------")
        
        # Save to a temporary log for calibration reference
        with open(os.path.join(BASE_DIR, "logs/acoustic_log.txt"), "a") as f:
            from datetime import datetime
            f.write(f"{datetime.now().isoformat()} | {volume} dB\n")
    else:
        sys.exit(1)
