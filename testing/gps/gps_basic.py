# requires sudo
# RX -> Pin 8
# TX -> Pin 10
import serial
from serial.serialutil import SerialException
from .gps_decoder import decodeGPGGA, NotGPGGAError

port = "/dev/serial0"

ser = serial.Serial(port, baudrate=9600, timeout=1.0)

while True:
    try:
        line = ser.readline()
        try:
            print(decodeGPGGA(line))
        except NotGPGGAError:
            pass
    except SerialException:
        print("Exception Raised!!")
        ser.close()
        ser = serial.Serial(port, baudrate=9600, timeout=1.0)
