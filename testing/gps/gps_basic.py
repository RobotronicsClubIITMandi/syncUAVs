# requires sudo
# RX -> Pin 8
# TX -> Pin 10
import serial

port = "/dev/serial0"

ser = serial.Serial(port, baudrate=9600, timeout=1.0)

while True:
    line = ser.readline().decode('ascii', errors='replace')
    print(line.strip())