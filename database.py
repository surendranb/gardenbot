import sqlite3
import os

DB_PATH = 'data/garden.db'

def init_db():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Sensor data table
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    temp REAL,
                    hum REAL,
                    soil INTEGER,
                    light INTEGER,
                    water_dist REAL,
                    water_vol REAL,
                    relay_status TEXT
                )''')
    
    # Photos table to track daily growth
    c.execute('''CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT,
                    note TEXT
                )''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
