import driver
from time import sleep
import os

# os.system('sudo pigpiod')

d = driver.Drone()


# program
try:
    d.arm()
    # d.spw(d.thr, 1450)
    sleep(2.0)
    # d.set_val(d.thr, 1600)
    # sleep(1.0)
    # d.set_val(d.thr, 1450)
    d.zeroall()
    d.disarm()
except KeyboardInterrupt:
    d.killall()

del d
