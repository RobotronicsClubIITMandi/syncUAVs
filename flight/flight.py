from gps_decoder import decodeGPGGA, FixNotAcquiredError, NotGPGGAError
from driver import Drone, pi
from serial.serialutil import SerialException
from multiprocessing import Process
import getch


class Flight:
    def __init__(self, bottomleft, topleft, topright, bottomright):
        self.bottomleft, self.topleft, self.topright, self.bottomright = (
            bottomleft,
            topleft,
            topright,
            bottomright,
        )
        self.d = Drone()
