import os
import picamera
from datetime import datetime
from subprocess import call
from time import sleep
from cookieClient6 import send
from time import time
from PIL import Image

picPath = "/home/pi/Desktop/"

def captureImage(picPath):
    # Generate the picture's name
    picName = 'image.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picPath + picName)
    print("We have taken a picture.")
    return picName

def findcolor(filePath):
    image = Image.open(filePath)
    c,r = image.size  #c = width, r = height
    pixelMap = image.load()
    ans = "Not recognized"      #Not recognized
    for i in range(r):
        for j in range(50):
            coordinate1 = j,i
            coordinate2 = c-j-1,i
            if (image.getpixel(coordinate1) == (0,255,0) or image.getpixel(coordinate2) == (0,255,0)):
                ans = "Recognized in Horizontal field of view"       #Recognized in Horizontal field of view
    for j in range(c):
        for i in range(50):
            coordinate1 = j,i
            coordinate2 = j,r-i-1
            if (image.getpixel(coordinate1) == (0,255,0) or image.getpixel(coordinate2) == (0,255,0)):
                ans = "Recognized in Vertical field of view"        #Recognized in Vertical field of view
    return ans

while True:
    picName = captureImage(picPath)
    print("Took a picture")
    completePath = picPath + picName
    print(completePath)
    ans = findcolor(completePath)
    send(ans)
    print("Color-Answer has been sent to PC :)")
    os.remove(completePath)
