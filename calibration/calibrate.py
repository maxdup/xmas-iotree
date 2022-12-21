import requests
import os
import sys
import inspect
from time import sleep
from datetime import datetime, timedelta

import numpy
import cv2
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# your camera is meant to be used in portrait mode, rotated 90 degrees ccw

from config import NLED


url = 'http://192.168.2.112/api/leds/'

lit = {'r':255, 'g':255, 'b':255}
unlit = {'r':0, 'g':0, 'b':0}
leds = [unlit] * 50

def sequenceAt(i):
    print('calibrating ' + str(i))
    leds = [unlit] * NLED
    leds[i] = lit
    requests.post(url, json={'colors': leds})

def screen_pos_to_coords(x,y):
    if CAM_ORIENTATION == 'PORTRAIT':
        return (y,x)
    else:
        return (x,y)


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


BLUR_RADIUS = 11


def auto_mode():
    delay = timedelta(seconds=0.5)
    coords = [None] * NLED
    i = 0
    sequenceAt(i)

    while (True):
        check, frame = cam.read()
        cv2.imshow('video', frame)

        key = cv2.waitKey(1)
        if key == 32: # spacebar, to start
            break

    sequenceAt(i)
    now = datetime.now()

    while (i < NLED):
        check, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (BLUR_RADIUS, BLUR_RADIUS), 0)

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(frame, maxLoc, BLUR_RADIUS, (255, 0, 0), 2)

        cv2.imshow('video', frame)

        key = cv2.waitKey(1)
        if key == 27: # spacebar, to start
            return None

        if (datetime.now() - now >= delay):
            coords[i] = screen_pos_to_coords(maxLoc[0], maxLoc[1])
            i += 1

            if i >= NLED:
                break

            sequenceAt(i)
            now = datetime.now()

    return coords

def assisted_mode():
    coords = [None] * NLED
    i = 0

    def mouseClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            nonlocal i
            print(flags)
            print(param)
            coords[i] = screen_pos_to_coords(x,y)
            i += 1
            print('click!')

    while (i < NLED):

        sequenceAt(i)
        check, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (BLUR_RADIUS, BLUR_RADIUS), 0)

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(frame, maxLoc, BLUR_RADIUS, (255, 0, 0), 2)

        cv2.namedWindow('Calibration')
        cv2.setMouseCallback('Calibration', mouseClick)

        cv2.imshow('Calibration', frame)

        key = cv2.waitKey(1)

        if key == 27: # esc key
            return None
        elif key == 32: # spacebar, to accept
            coords[i] = screen_pos_to_coords(maxLoc[0], maxLoc[1])
            i += 1
        elif key == 92: # \, to reject
            coords[i] = None
            i += 1
        elif key == 8: # backspace, to undo
            i -= 1

    return coords


MODE = 'assisted' # ['AUTO', 'ASSISTED', 'MANUAL']
CAM_ORIENTATION = 'portrait' # ['PORTRAIT', 'LANDSCAPE']
CAM_POSITION = 'Xplus' # ['Xplus', 'xMinus', 'yPlus', 'yMinux']

if MODE == 'ASSISTED':
    coords = assisted_mode()
elif MODE == 'AUTO':
    coords = auto_mode()

print(coords)

