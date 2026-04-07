import serial
import time
import sys
import argparse

PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_diagnostics(fast=False, duration=60):
    delay = 0.25 if fast else 1.0
    iterations = int(duration / delay)
    
    print(f"--- GardenOS High-Speed Signal Audit ---")
    print(f"Polling {PORT} @ {delay}s intervals...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)
        ser.flushInput()
        
        recovered = False
        for i in range(iterations):
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line: continue
                
                parts = line.split('|')
                if len(parts) < 8: continue
                
                press = float(parts[6])
                if press > 900:
                    if not recovered:
                        print("\n✨ [SIGNAL ACQUIRED] BME680 is reporting valid pressure!")
                        recovered = True
                    sys.stdout.write("█")
                else:
                    sys.stdout.write("░")
                sys.stdout.flush()
                
                if i % 20 == 0:
                    print(f" [RAW: {line}]")
            except Exception:
                continue
                
            time.sleep(delay)
            
        print("\n" + "-" * 50)
        print("Audit Complete.")
            
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()
    run_diagnostics(fast=args.fast)

if __name__ == "__main__":
    run_diagnostics()
