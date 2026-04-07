#!/usr/bin/env python3
import serial
import time
import sys

# Configuration
PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_pulse_test():
    print(f"--- 🌿 GardenOS Pulse Test (5 Samples) ---")
    print(f"Connecting to {PORT}...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=3)
        time.sleep(2) # Initial reset grace
        ser.reset_input_buffer()
        
        recovered_any = False
        for i in range(10):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 8:
                    press = float(parts[6])
                    status = "✅ ONLINE" if press > 900 else "❌ ZERO"
                    if status == "✅ ONLINE": recovered_any = True
                    print(f"Pulse {i+1}: {parts[0]}°C | {parts[1]}% | {parts[6]} hPa | {parts[7]} kΩ [{status}]")
                else:
                    print(f"Pulse {i+1}: Malformed Line")
            else:
                print(f"Pulse {i+1}: No Signal")
            
            time.sleep(2) # 2s gap between samples
            
        print("-" * 40)
        if recovered_any:
            print("✨ SIGNAL RECOVERED: The BME680 is live.")
        else:
            print("🌑 STILL SILENT: I2C is not responding.")
            
        ser.close()
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    run_pulse_test()
