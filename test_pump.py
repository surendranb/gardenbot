import serial
import time

SERIAL_PORT = '/dev/cu.usbmodem312301'
BAUD_RATE = 9600

def test_pump():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connecting to Arduino on {SERIAL_PORT}...")
        time.sleep(2) # Wait for Arduino to reset
        
        print("Sending WATER_ON command...")
        ser.write(b"WATER_ON\n")
        
        # Keep it on for 3 seconds
        time.sleep(3)
        
        print("Sending WATER_OFF command...")
        ser.write(b"WATER_OFF\n")
        
        print("Test Complete.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pump()
