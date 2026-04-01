import serial.tools.list_ports
for p in serial.tools.list_ports.comports():
    print(f"Device: {p.device}, Description: {p.description}, HWID: {p.hwid}")
