import serial
import time
import sys
import argparse

PORT = "/dev/cu.usbmodem1201"
BAUD = 9600

def run_diagnostics(fast=False, duration=60, delay=None):
    if delay is None:
        delay = 0.25 if fast else 1.0
    iterations = int(duration / delay)
    
    print(f"--- GardenOS High-Speed Signal Audit ---")
    print(f"Polling {PORT} @ {delay}s intervals (Total: {iterations} readings)...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        # BME680 Boot Protocol: 3.0s settle delay (PROJECT_SILICA.md)
        print("Executing Boot Protocol: 3.0s settle delay...")
        time.sleep(3)
        ser.flushInput()
        
        recovered = False
        for i in range(iterations):
            try:
                # ser.flushInput() # Optional: clear buffer for real-time truth
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    print(f"[{i+1}/{iterations}] [NO DATA] Polling...")
                else:
                    print(f"[{i+1}/{iterations}] RAW: {line}")
                    
                    parts = line.split('|')
                    if len(parts) >= 8:
                        press = float(parts[6])
                        if press > 900:
                            if not recovered:
                                print("\n✨ [SIGNAL ACQUIRED] BME680 is reporting valid pressure!")
                                recovered = True
                            sys.stdout.write("█")
                        else:
                            sys.stdout.write("░")
                        sys.stdout.flush()
            except Exception as e:
                print(f"Error during poll: {e}")
                
            time.sleep(delay)
            
        print("\n" + "-" * 50)
        print("Audit Complete.")
            
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--delay", type=float, default=None)
    parser.add_argument("--readings", type=int, default=None)
    args = parser.parse_args()
    
    duration = args.duration
    delay = args.delay
    
    if args.readings:
        delay = duration / args.readings
        
    run_diagnostics(fast=args.fast, duration=duration, delay=delay)
