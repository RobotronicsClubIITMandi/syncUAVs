import socket
from time import sleep
from time import time

host = '192.168.43.229'    #IP address of Server(PC) over a single Hotspot or n$
port = 5566

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendans(s, ans):
    s.send(str.encode(ans))
    print("Done sending")
    return "Done sending"

s = setupSocket()

def send(ans):
    response = sendans(s, ans)
    return response
