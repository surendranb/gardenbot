import serial
import sqlite3
import time
import math
from dashboard_gen import generate_dashboard

# Configuration
SERIAL_PORT = '/dev/cu.usbmodem312301'
BAUD_RATE = 9600
DB_NAME = 'data/garden.db'

# Tank dimensions in cm (Edit these to match your container)
TANK_HEIGHT = 15.0 # Total height of tank
TANK_RADIUS = 5.0 # Radius of tank

def calculate_volume(distance):
    # Calculate water depth (total height minus empty space distance)
    depth = max(0, TANK_HEIGHT - distance)
    # Cylinder volume: pi * r^2 * h
    volume = math.pi * (TANK_RADIUS**2) * depth
    return round(volume, 2) # Volume in cubic cm (same as ml)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (timestamp REAL, temp REAL, hum REAL, soil INTEGER, light INTEGER, water_dist REAL, water_vol REAL, relay_status TEXT)''')
    conn.commit()
    conn.close()

def log_data():
    init_db()
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Logging data to {DB_NAME}... Press Ctrl+C to stop.")
        
        print("Starting 3-second Pump Test...")
        ser.write(b"WATER_ON\n")
        time.sleep(3)
        ser.write(b"WATER_OFF\n")
        print("Pump Test Complete.")
        
        start_time = time.time()
        while time.time() - start_time < 30:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) == 6:
                        t, h, s, l, wd, rs = parts
                        vol = calculate_volume(float(wd))
                        
                        # Log to console
                        print(f"[{time.strftime('%H:%M:%S')}] Temp: {t}C | Hum: {h}% | Soil: {s} | Water: {vol}ml ({wd}cm distance) | Light: {l} | Pump: {rs}")
                        
                        # Save to SQLite
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("INSERT INTO sensor_data (timestamp, temp, hum, soil, light, water_dist, water_vol, relay_status) VALUES (?,?,?,?,?,?,?,?)", 
                                  (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), t, h, s, l, wd, vol, rs))
                        conn.commit()
                        conn.close()
                        
                        # Regenerate the static dashboard
                        generate_dashboard()
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    log_data()
