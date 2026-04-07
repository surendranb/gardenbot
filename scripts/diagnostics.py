#!/usr/bin/env python3
import serial
import time
import sys

PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_diagnostics():
    print(f"--- GardenOS Hardware Diagnostic Tool ---")
    print(f"Connecting to {PORT}...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=3)
        time.sleep(2)  # Wait for Arduino reset
        ser.flushInput()
        
        print("Listening for 8-part telemetry stream...")
        print("Format: TEMP|HUM|LIGHT|P1|P3|P2|PRESS|GAS")
        print("-" * 50)
        
        stable_count = 0
        for i in range(30):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                print(f"[{i+1}/30] TIMEOUT: No data received.")
                continue
            
            parts = line.split('|')
            if len(parts) != 8:
                print(f"[{i+1}/30] MALFORMED: {line}")
                continue
                
            # Parse for health
            try:
                temp = float(parts[0])
                hum = float(parts[1])
                press = float(parts[6])
                gas = float(parts[7])
                
                bme_status = "✅ ONLINE" if press > 900 else "❌ ERROR (0.0)"
                if bme_status == "✅ ONLINE": stable_count += 1
                
                print(f"[{i+1}/30] RAW: {line}")
                print(f"       BME680: {bme_status} | T: {temp}°C | H: {hum}% | P: {press}hPa | G: {gas}kΩ")
            except ValueError:
                print(f"[{i+1}/30] PARSE ERROR: {line}")
                
            time.sleep(1)
            
        print("-" * 50)
        print(f"Diagnostics Complete. Stability: {stable_count}/30 valid BME680 pulses.")
        if stable_count < 25:
            print("⚠️ WARNING: Intermittent signal detected. Check I2C (A4/A5) jumpers.")
        else:
            print("✨ Hardware connection appears stable.")
            
    except Exception as e:
        print(f"FATAL ERROR: {e}")
    finally:
        if 'ser' in locals(): ser.close()

if __name__ == "__main__":
    run_diagnostics()
