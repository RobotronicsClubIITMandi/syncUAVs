from time import sleep
import pigpio

pi = pigpio.pi()


class Drone:
    def __init__(self):
        self.ail = 5
        self.ele = 6
        self.thr = 13
        self.rud = 19
        self.aux = 26
        self.ch = [5, 6, 13, 19, 26]
        self.thr_start = 1450
        self.ch_name = ["ail", "ele", "thr", "rud", "aux"]
        self.zeros = {"ail": 1504, "ele": 1504, "thr": 1164, "rud": 1504, "aux": 1505}
        self.mins = {"ail": 1124, "ele": 1185, "thr": 1410, "rud": 1110, "aux": 1020}
        self.maxs = {"ail": 1852, "ele": 1820, "thr": 1850, "rud": 1924, "aux": 2050}
        self.inc = 10
        self.spw = pi.set_servo_pulsewidth
        self.initialize()

    def initialize(self):
        for c in self.ch:
            pi.set_mode(c, pigpio.OUTPUT)
        for c, cname in zip(self.ch, self.ch_name):
            pi.set_servo_pulsewidth(c, self.zeros[cname])

    def arm(self):
        pi.set_servo_pulsewidth(self.thr, 500)
        pi.set_servo_pulsewidth(self.rud, self.mins["rud"])
        sleep(2.0)
        pi.set_servo_pulsewidth(self.rud, self.zeros["rud"])
        pi.set_servo_pulsewidth(self.thr, self.zeros["thr"])

    def disarm(self):
        self.set_val(self.thr, self.zeros["thr"])
        pi.set_servo_pulsewidth(self.thr, 500)
        pi.set_servo_pulsewidth(self.rud, self.maxs["rud"])
        sleep(2.0)
        pi.set_servo_pulsewidth(self.rud, self.zeros["rud"])
        pi.set_servo_pulsewidth(self.thr, self.zeros["thr"])

    def killall(self):
        self.disarm()
        for c in self.ch:
            pi.set_servo_pulsewidth(c, 0)

    def zeroall(self):
        for c, cname in zip(self.ch, self.ch_name):
            pi.set_servo_pulsewidth(c, self.zeros[cname])

    def set_val(self, c, final_val, sleep_time=0.05):
        start_val = pi.get_servo_pulsewidth(c)

        if final_val > self.maxs[self.get_name(c)]:
            final_val = self.maxs[self.get_name(c)]
        elif final_val < self.mins[self.get_name(c)]:
            final_val = self.mins[self.get_name(c)]

        if start_val <= final_val:
            inc = self.inc
        else:
            inc = -self.inc
        for i in range(start_val, final_val, inc):
            pi.set_servo_pulsewidth(c, i)
            sleep(sleep_time)
        pi.set_servo_pulsewidth(c, final_val)

        return final_val

    def set_val_danger(self, c, final_val, sleep_time=0.02):
        start_val = pi.get_servo_pulsewidth(c)
        if start_val <= final_val:
            inc = self.inc
        else:
            inc = -self.inc
        for i in range(start_val, final_val, inc):
            pi.set_servo_pulsewidth(c, i)
            sleep(sleep_time)
        pi.set_servo_pulsewidth(c, final_val)

        return final_val

    def change_val(self, c, change):
        final_val = pi.get_servo_pulsewidth(c) + change
        return self.set_val(c, final_val)

    def startup(self):
        pi.set_servo_pulsewidth(self.thr, self.thr_start)
        self.set_val(self.thr, self.mins["thr"], 0.2)

    def get_c(self, name):
        i = self.ch_name.index(name)
        return self.ch[i]

    def get_name(self, c):
        i = self.ch.index(c)
        return self.ch_name[i]

    def control(self, inp):
        if inp == "w":
            print("thr", self.change_val(self.thr, 15))
        elif inp == "s":
            print("thr", self.change_val(self.thr, -15))
        elif inp == "2":
            print("DISARMED")
            self.disarm()
        elif inp == "1":
            print("ARMED")
            self.arm()
        elif inp == "i":
            print("ele", self.change_val(self.ele, 5))
        elif inp == "k":
            print("ele", self.change_val(self.ele, -5))
        elif inp == "j":
            print("ail", self.change_val(self.ail, -5))
        elif inp == "l":
            print("ail", self.change_val(self.ail, 5))
        elif inp == "0":
            print("ail & ele reset")
            pi.set_servo_pulsewidth(self.ail, self.zeros["ail"])
            pi.set_servo_pulsewidth(self.ele, self.zeros["ele"])
        else:
            pass
