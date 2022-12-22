import requests
import os
import sys
import inspect
import json
import argparse

from time import sleep
from datetime import datetime, timedelta

import numpy
import random
import cv2
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import NLED


AUTO_MODE_INSTRUCTIONS = '''
Controls for auto mode:
  Spacebar  - Starts the scan
  Esc       - Stop/cancels the scan
'''

ASSISTED_MODE_INSTRUCTIONS = '''
Controls for assisted mode:
  Spacebar    - use the suggested coordinate
  left-click  - use the clicked area for coordinate
  backspace   - undo the last coord
  \           - Omits the value for this coordinate (None)
  Esc         - stop/cancels the scan
'''

BLUR_RADIUS = 11
COORDFILE = 'raw_coordinates.json'

cam_orientation = None
cam_h = None
cam_w = None
led_url = None

lit = {'r':255, 'g':255, 'b':255}
unlit = {'r':0, 'g':0, 'b':0}
leds = [unlit] * 50

cam = cv2.VideoCapture(0)

def sequenceAt(i):
    i = min(len(leds)-1, max(0, i))
    print('calibrating {}/{}'.format(i+1, NLED))

    leds = [unlit] * NLED
    leds[i] = lit
    requests.post(led_url, json={'colors': leds})

def make_window(mode):
    check, frame = cam.read()
    windowName = 'Calibration - {}'.format(mode)
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.imshow(windowName, frame)

    portrait = cam_orientation == 'portrait'
    w_w, w_h =  (cam_h, cam_w) if portrait else (cam_w, cam_h)
    cv2.resizeWindow(windowName, w_w, w_h)

    cv2.imshow(windowName, frame)
    return windowName


def make_frame(window):
    check, frame = cam.read()
    if cam_orientation == 'portrait':
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (BLUR_RADIUS, BLUR_RADIUS), 0)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    portrait = cam_orientation == 'portrait'
    w_w, w_h =  (cam_h, cam_w) if portrait else (cam_w, cam_h)
    cv2.line(frame, (int(w_w/2),0), (int(w_w/2),w_h), (255, 255, 255, 0.5), 2)
    cv2.circle(frame, maxLoc, BLUR_RADIUS, (0, 0, 255), 2)
    cv2.imshow(window, frame)
    return maxLoc

def assisted_mode():
    window = make_window('Assisted')
    coords = [None] * NLED
    i = 0

    def mouseClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            nonlocal i
            coords[i] = (x,y)
            i += 1
    cv2.setMouseCallback(window, mouseClick)

    sequenceAt(i)

    while (i < NLED):
        coord = make_frame(window)
        key = cv2.waitKey(1)

        if key == 27: # esc, to exit
            return None
        elif key == 32: # spacebar, to accept
            coords[i] = coord
            i += 1
            sequenceAt(i)
        elif key == 92: # \, to reject
            coords[i] = None
            i += 1
            sequenceAt(i)
        elif key == 8: # backspace, to undo
            i -= 1
            sequenceAt(i)

    return coords

def auto_mode():
    window = make_window('Auto')
    delay = timedelta(seconds=0.5)
    coords = [None] * NLED
    i = 0
    sequenceAt(i)

    while (True):
        make_frame(window)
        key = cv2.waitKey(1)

        if key == 32: # spacebar, to start
            break
        if key == 27: # esc, to exit
            return None

    sequenceAt(i)
    now = datetime.now()

    while (i < NLED):
        coord = make_frame(window)

        key = cv2.waitKey(1)
        if key == 27: # esc, to exit
            return None

        if (datetime.now() - now >= delay):
            coords[i] = coord
            i += 1

            if i >= NLED:
                break

            sequenceAt(i)
            now = datetime.now()

    return coords

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Coordinates for your set of leds')

    parser.add_argument('angle', choices=['xpos', 'ypos', 'xneg', 'yneg'],
                        help='The angle of the capture.')

    parser.add_argument('url',
                        help='The api endpoint that controls your leds (ex: http://192.168.1.11/api/leds/).')

    parser.add_argument('-m', '--mode', choices=['assisted', 'auto', 'mock'],
                        default="assisted", help='The scanning mode')

    parser.add_argument('-co', '--cam-orientation', choices=['portrait', 'landscape' ],
                        default="portrait", help='The orientation of the capture.')

    parser.add_argument('-ch', '--cam-height', type=int,
                        default=1080, help='The height of the camera resolution.')

    parser.add_argument('-cw', '--cam-width', type=int,
                        default=1980, help='The width of the camera resolution.')


    args = parser.parse_args()

    cam_orientation = args.cam_orientation
    cam_h = args.cam_height
    cam_w = args.cam_width
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_w)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_h)

    led_url = args.url

    if args.mode == 'assisted':
        print(ASSISTED_MODE_INSTRUCTIONS)
        coords = assisted_mode()
    elif args.mode == 'auto':
        print(AUTO_MODE_INSTRUCTIONS)
        coords = auto_mode()
    elif args.mode == 'mock':
        coords = [(random.randrange(0,100),
                   random.randrange(0,100),
                   random.randrange(0,100)) for i in range(NLED)]

    filecoords = {}
    if os.path.exists(COORDFILE):
        with open(COORDFILE, 'r+') as f:
            content = f.read() or '{}'
            filecoords = json.loads(content)

    filecoords[args.angle] = coords

    with open(COORDFILE, 'w+') as f:
        f.write(json.dumps(filecoords))
