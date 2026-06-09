#!/usr/bin/env python3
import serial
import time
import os
import json
from datetime import datetime

STATE_FILE = "/Users/surendran/.openclaw/workspace/gardenbot/data/bme_state.json"
PORT = '/dev/cu.usbmodem11201'

def main():
    print(f"Starting BME680 Continuous Daemon on {PORT}...")
    
    while True:
        try:
            # Keep connection open permanently to avoid DTR resets and allow heater to stabilize
            with serial.Serial(PORT, 9600, timeout=10) as ser:
                ser.setDTR(False)
                time.sleep(1)
                ser.setDTR(True)
                time.sleep(4) # Initial boot delay
                
                print("Connection established. Heating sensor...")
                
                while True:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 6:
                            try:
                                t, h, l, a2, p, g = map(float, parts)
                                
                                # Ignore dead bus or saturation artifacts
                                if (t == 0.0 and h == 0.0) or (p == 652.01 and h == 100.0):
                                    continue
                                
                                # Write valid state to JSON for other agents to read instantly
                                state = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "temp": t,
                                    "hum": h,
                                    "light": int(l),
                                    "p2_jade": int(a2),
                                    "press": p,
                                    "gas": g
                                }
                                
                                # Atomic write to prevent read collisions
                                tmp_file = STATE_FILE + ".tmp"
                                with open(tmp_file, "w") as f:
                                    json.dump(state, f)
                                os.rename(tmp_file, STATE_FILE)
                                
                            except ValueError:
                                pass # Ignore malformed serial lines
                                
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Daemon connection error: {e}. Retrying in 10s...")
            time.sleep(10)

if __name__ == "__main__":
    main()
