#!/usr/bin/env python3
import serial
import time
import sys

PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_raw_dump():
    print(f"--- 📡 GardenOS Raw Diagnostic Dump ---")
    print(f"Attempting to listen to {PORT} for 10 seconds...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2) # Reset time
        
        start_time = time.time()
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                char = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                sys.stdout.write(char)
                sys.stdout.flush()
            time.sleep(0.1)
            
        print("\n\n" + "-" * 40)
        print("Raw Dump Complete.")
        ser.close()
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    run_raw_dump()
