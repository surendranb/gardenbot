import serial
import sqlite3
import time
import os
import glob
from datetime import datetime
from PIL import Image
from dashboard_gen import generate_dashboard

# Configuration
SERIAL_PORT = '/dev/cu.usbmodem312301'
BAUD_RATE = 9600
DB_NAME = 'data/garden.db'
PHOTO_DIR = 'photos/'

# Tank dimensions (Coffee Sipper: ~400ml)
SIPPER_HEIGHT = 15.0 # cm
SIPPER_RADIUS = 3.0 # cm

def get_latest_photo():
    photos = glob.glob(os.path.join(PHOTO_DIR, '*.[jp][pg]*')) # jpg, jpeg, png
    if not photos:
        return None
    return max(photos, key=os.path.getctime)

def calculate_sipper_vol(distance):
    # Depth = Total Height - Empty Space
    depth = max(0, min(SIPPER_HEIGHT, SIPPER_HEIGHT - distance))
    # Volume = pi * r^2 * depth (in ml)
    vol = 3.14159 * (SIPPER_RADIUS**2) * depth
    return round(vol, 1)

def log_pulse():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pulse starting...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2) # Wait for reset
        
        # Read a few lines to clear buffer and get fresh data
        for _ in range(5):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        if "|" in line:
            parts = line.split("|")
            if len(parts) == 6:
                t, h, s, l, wd, rs = parts
                vol = calculate_sipper_vol(float(wd))
                
                # Check for today's photo
                today_str = datetime.now().strftime('%Y-%m-%d')
                photo = get_latest_photo()
                has_today_photo = today_str in photo if photo else False
                
                # Save to database
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("""INSERT INTO sensor_data 
                            (timestamp, temp, hum, soil, light, water_dist, water_vol, relay_status) 
                            VALUES (?,?,?,?,?,?,?,?)""",
                          (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), t, h, s, l, wd, vol, rs))
                
                # If a photo was added, log it in the photos table if not already there
                if photo and not has_today_photo:
                     c.execute("INSERT OR IGNORE INTO photos (timestamp, file_path) VALUES (?,?)",
                              (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), photo))
                
                conn.commit()
                conn.close()
                
                print(f"Pulse Success: Soil {s} | Water {vol}ml | Photo Today: {has_today_photo}")
                
                # Regenerate dashboard
                generate_dashboard()
                
        ser.close()
    except Exception as e:
        print(f"Pulse Failed: {e}")

if __name__ == "__main__":
    log_pulse()
