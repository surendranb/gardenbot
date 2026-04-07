#!/usr/bin/env python3
import serial
import time
import sys

# Configuration
PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_raw_watch():
    print(f"--- 📡 GardenOS 20s Live Hardware Watch ---")
    print(f"Watching {PORT} (9600)... Jiggle your wires now!")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2) # Reset grace
        ser.reset_input_buffer()
        
        start_time = time.time()
        while time.time() - start_time < 20:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                if "|" in line:
                    parts = line.split("|")
                    temp = parts[0]
                    press = parts[6] if len(parts) > 6 else "0.0"
                    status = "✅" if float(press) > 900 else "░"
                    print(f"[{status}] {line}")
                else:
                    print(f"[-] {line}")
                sys.stdout.flush()
            
        print("-" * 40)
        print("Hardware Watch Complete.")
        ser.close()
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    run_raw_watch()
