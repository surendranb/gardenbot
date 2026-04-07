#!/usr/bin/env python3
import serial
import time
import sys

# Configuration
PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_30_sample_watch():
    print(f"--- 📡 GardenOS 30-Sample 'Truth' Watch ---")
    print(f"Sampling every 2s for 60 seconds... Adjust your hardware now!")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=3)
        time.sleep(2) # Initial reset
        ser.reset_input_buffer()
        
        for i in range(1, 31):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                if "|" in line:
                    parts = line.split("|")
                    press = parts[6] if len(parts) > 6 else "0"
                    # We check for valid pressure > 900 hPa
                    is_valid = float(press) > 900
                    icon = "✅" if is_valid else "░"
                    print(f"Sample {i:02}: [{icon}] {line}")
                else:
                    print(f"Sample {i:02}: [-] {line}")
                sys.stdout.flush()
            else:
                print(f"Sample {i:02}: No Signal")
            
        print("-" * 40)
        print("Hardware Watch Complete.")
        ser.close()
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    run_30_sample_watch()
