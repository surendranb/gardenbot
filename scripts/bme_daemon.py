#!/usr/bin/env python3
import serial
import time
import os
import json
from datetime import datetime, timedelta

STATE_FILE = "/Users/surendran/.openclaw/workspace/gardenbot/data/bme_state.json"
PORT = '/dev/cu.usbmodem11201'
GRACE_PERIOD_MINUTES = 15

def main():
    print(f"Starting BME680 Resilient Daemon on {PORT}...")
    
    last_good_bme = {
        "temp": None, "hum": None, "press": None, "gas": None, "timestamp": None
    }
    
    while True:
        try:
            with serial.Serial(PORT, 9600, timeout=10) as ser:
                ser.setDTR(False)
                time.sleep(1)
                ser.setDTR(True)
                time.sleep(4)
                
                print("Connection established. Listening to telemetry stream...")
                
                while True:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 6:
                            try:
                                t, h, l, a2, p, g = map(float, parts)
                                now = datetime.now()
                                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                                
                                # 1. Detect BME680 Failure (Dead Bus or Saturation)
                                bme_failed = (t == 0.0 and h == 0.0) or (p == 652.01 and h == 100.0)
                                
                                if not bme_failed:
                                    # Update Last Known Good State
                                    last_good_bme = {
                                        "temp": t, "hum": h, "press": p, "gas": g, "timestamp": now
                                    }
                                
                                # 2. Graceful Degradation Logic
                                bme_status = "OK"
                                out_t, out_h, out_p, out_g = t, h, p, g
                                
                                if bme_failed:
                                    if last_good_bme["timestamp"] and (now - last_good_bme["timestamp"]) < timedelta(minutes=GRACE_PERIOD_MINUTES):
                                        # Use cached values within grace period
                                        bme_status = "CACHED (Grace Period)"
                                        out_t = last_good_bme["temp"]
                                        out_h = last_good_bme["hum"]
                                        out_p = last_good_bme["press"]
                                        out_g = last_good_bme["gas"]
                                    else:
                                        # Grace period expired, report hard failure (use None/NaN, not zeros)
                                        bme_status = "OFFLINE"
                                        out_t = out_h = out_p = out_g = None

                                # 3. Construct the Resilient State Payload
                                # Analog sensors (Light, Soil) are ALWAYS reported, even if BME is dead.
                                state = {
                                    "timestamp": now_str,
                                    "status": bme_status,
                                    "temp": out_t,
                                    "hum": out_h,
                                    "light": int(l),
                                    "p2_jade": int(a2),
                                    "press": out_p,
                                    "gas": out_g
                                }
                                
                                # 4. Atomic Write
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
