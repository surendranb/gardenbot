#!/usr/bin/env python3
import sqlite3
import json
import os
import shutil
from datetime import datetime

BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
DB_PATH = os.path.join(BASE_DIR, "data/garden.db")
PUBLIC_DIR = os.path.join(BASE_DIR, "dashboard/public")

def build():
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    if not os.path.exists(DB_PATH):
        print("Database not found. Skipping static build.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Query telemetry (last 150 for 72h range)
    cursor.execute("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 150")
    telemetry = [dict(row) for row in cursor.fetchall()]
    
    # 2. Query weather (last 50)
    cursor.execute("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 50")
    weather = [dict(row) for row in cursor.fetchall()]
    
    # 3. Query vision (last 20)
    cursor.execute("SELECT * FROM vision ORDER BY timestamp DESC LIMIT 20")
    vision = [dict(row) for row in cursor.fetchall()]
    
    # 4. Query interpretations (last 20)
    cursor.execute("SELECT * FROM interpretations ORDER BY timestamp DESC LIMIT 20")
    interpretations = [dict(row) for row in cursor.fetchall()]
    
    # 5. Query human actions (last 20)
    cursor.execute("SELECT * FROM human_actions ORDER BY timestamp DESC LIMIT 20")
    human_actions = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    payload = {
        "telemetry": telemetry[::-1],
        "weather": weather,
        "vision": vision,
        "interpretations": interpretations,
        "human_actions": human_actions
    }
    
    # Write data.json to public
    data_path = os.path.join(PUBLIC_DIR, "data.json")
    with open(data_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Static data exported to {data_path}")
    
    # Copy latest image to public (from data/latest.jpg if it exists)
    latest_img_src = os.path.join(BASE_DIR, "data/latest.jpg")
    latest_img_dest = os.path.join(PUBLIC_DIR, "latest.jpg")
    if os.path.exists(latest_img_src):
        import shutil
        shutil.copy2(latest_img_src, latest_img_dest)
        print(f"Copied latest image to {latest_img_dest}")

if __name__ == "__main__":
    build()
