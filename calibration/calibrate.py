import requests
import os
import sys
import inspect
from time import sleep

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import NLED

url = 'http://192.168.2.112/api/leds/'
leds = []

lit = {'r':255, 'g':255, 'b':255}
unlit = {'r':0, 'g':0, 'b':0}

def send():
    requests.post(url, json={'colors': leds})

for i in range(NLED):
    leds.append(unlit)

send()

for i in range(NLED):
    print('calibrating ' + str(i))
    leds[max(0,i-1)] = unlit
    leds[i] = lit
    send()
    sleep(0.5)


