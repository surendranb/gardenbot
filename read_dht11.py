import serial
import time

# Update the port to match the one we found
SERIAL_PORT = '/dev/cu.usbmodem312301'
BAUD_RATE = 9600

def read_from_arduino():
    try:
        # Initialize serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        
        # Give the connection a moment to settle
        time.sleep(2)
        
        start_time = time.time()
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Data received: {line}")
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
    except KeyboardInterrupt:
        print("\nStopping read operation...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    read_from_arduino()
