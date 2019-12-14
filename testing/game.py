import driver
from time import sleep
import getch

d = driver.Drone()
respose = 10.0

try:
    d.arm()
    # d.startup()
    while True:
        d.control(str(getch.getch()))
        continue
except KeyboardInterrupt:
    d.killall()
