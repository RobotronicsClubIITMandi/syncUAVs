import driver
from time import sleep
from multiprocessing import Process, Queue
import getch
import serial
from serial.serialutil import SerialException
from gps_decoder import decodeGPGGA, NotGPGGAError, FixNotAcquiredError, haversine

gps_port = "/dev/serial0"
ser = serial.Serial(gps_port, baudrate=9600, timeout=1.0)

bottomleft = (0, 0)
topleft = (0, 0)
topright = (0, 0)
bottomright = (0, 0)


def gpsloop(mpq):
    global ser
    while True:
        try:
            line = ser.readline()
            try:
                vals = decodeGPGGA(line)
                mpq.put(vals)
            except NotGPGGAError:
                pass
            except FixNotAcquiredError:
                print("GPS fix not acquired")
        except SerialException:
            print("Exception Raised!!")
            ser.close()
            ser = serial.Serial(gps_port, baudrate=9600, timeout=1.0)


if __name__ == "__main__":
    d = driver.Drone()
    mpq = Queue()
    gps_proc = Process(target=gpsloop, args=(mpq,))
    gps_proc.start()
    print("Press 's' to start")
    while str(getch.getch()) != "s":
        pass

    try:
        d.arm()
        d.startup()
        print(d.set_val_ratio(d.thr, 1.3 * d.thr_stable_ratio))
        sleep(0.9)
        print(d.set_val_ratio(d.thr, d.thr_stable_ratio))

        print(d.set_val_ratio(d.ele, 0.05))
        sleep(1.0)
        d.control("0")
        print(d.set_val_ratio(d.ail, 0.05))
        sleep(1.0)
        d.control("0")
        print(d.set_val_ratio(d.ele, -0.05))
        sleep(1.0)
        d.control("0")

        print(d.set_val_ratio(d.thr, 0.85 * d.thr_stable_ratio))
        sleep(3.0)
        d.disarm()
    except KeyboardInterrupt:
        d.disarm()
