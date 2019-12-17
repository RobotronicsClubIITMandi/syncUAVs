import driver
from time import sleep
import getch
from multiprocessing import Process

# from gps import decodeGPGGA, NotGPGGAError, FixNotAcquiredError


class WaitTimeException(Exception):
    pass


d = driver.Drone()
waittime = 7.0
ignore_range = False


def sleep_throw_exception(wait):
    sleep(wait)
    print("RESPONSE TIME EXCEEDED")
    raise WaitTimeException


# def gps_out():
#     port = "/dev/serial0"
#     ser = serial.Serial(port, baudrate=9600, timeout=1.0)

#     while True:
#         try:
#             line = ser.readline()
#             try:
#                 print(decodeGPGGA(line))
#             except NotGPGGAError:
#                 pass
#             except FixNotAcquiredError:
#                 print("GPS fix not acquired")
#         except SerialException:
#             print("GPS serial Exception Raised!!")
#             ser.close()
#             ser = serial.Serial(port, baudrate=9600, timeout=1.0)

try:
    d.arm()
    # gps_process = Process(target=gps_out)
    print("GIVE INPUTS!!")
    # d.startup()
    while True:
        pr = Process(target=sleep_throw_exception, args=(waittime,))
        pr.start()
        try:
            command = str(getch.getch())
            pr.terminate()
            if command == "c":
                ignore_range = not ignore_range
                print("ignore range :", ignore_range)
            else:
                d.control(command, ignore_range=ignore_range)
        except WaitTimeException:
            d.control("0")
            d.startup()
            sleep(5.0)
            d.disarm()

except KeyboardInterrupt:
    d.disarm()
