#!/usr/bin/env python3
import subprocess
import re
import os
import sys

def get_mic_index():
    """Scans for the USB2.0 MIC and returns its index."""
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/ffmpeg", "-list_devices", "true", "-f", "avfoundation", "-i", "dummy"],
            stderr=subprocess.PIPE, text=True, timeout=10
        )
        if "AVFoundation audio devices:" in result.stderr:
            audio_section = result.stderr.split("AVFoundation audio devices:")[1]
            match = re.search(r"\[(\d+)\] USB2.0 MIC", audio_section)
            if match:
                return match.group(1)
    except Exception:
        pass
    return "0"

MIC_INDEX = get_mic_index()
DURATION = 5 # seconds
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"

def capture_volume():
    """Captures audio and returns the mean volume in dB."""
    print(f"Listening to the room for {DURATION} seconds...")
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
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, timeout=10)
        output = result.stderr
        match = re.search(r"mean_volume: ([\-\d.]+) dB", output)
        if match:
            return float(match.group(1))
        else:
            print("Error: Could not find mean_volume in ffmpeg output.")
            return None
    except Exception as e:
        print(f"Acoustic Capture Failed: {e}")
        return None

if __name__ == "__main__":
    volume = capture_volume()
    if volume is not None:
        print(f"Mean Volume: {volume} dB")
        # Log it
        log_file = os.path.join(BASE_DIR, "logs/acoustic_log.txt")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        from datetime import datetime
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} | {volume} dB\n")
    else:
        sys.exit(1)
