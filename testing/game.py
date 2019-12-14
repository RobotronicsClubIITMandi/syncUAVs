import driver
from time import sleep
import getch
from multiprocessing import Process


class WaitTimeException(Exception):
    pass


d = driver.Drone()
waittime = 5.0


def sleep_throw_exception(wait):
    sleep(wait)
    print("RESPONSE TIME EXCEEDED")
    raise WaitTimeException


try:
    d.arm()
    print("GIVE INPUTS!!")
    # d.startup()
    while True:
        pr = Process(target=sleep_throw_exception, args=(waittime,))
        try:
            d.control(str(getch.getch()))
            pr.terminate()
        except WaitTimeException:
            d.control("0")
            d.startup()
            sleep(5.0)
            d.disarm()

except KeyboardInterrupt:
    d.killall()
