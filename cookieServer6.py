import socket
from time import sleep
import os
host = ''
port = 5566

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(100) # Allows one connection at a time. You can increase for more no. of clients
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))    #IP and Port No.
    return conn


def datarecieve(conn):
    while True:
        # Receive the data
        ans = conn.recv(1024) # receive the data
        print(ans.decode("utf-8"))
        # Send the reply back to the client
        conn.sendall(str.encode("Recieved"))
    conn.close()

s = setupServer()

while True:
    try:
        conn = setupConnection()
        datarecieve(conn)
    except:
        break
