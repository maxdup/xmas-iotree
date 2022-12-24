import board
import neopixel
from time import sleep
import math
import json

with open('/var/www/xmas-iotree/coordinates.json', 'r+') as f:
    coords = json.loads(f.read() or '{}')
    NLED = len(coords)

pixels = neopixel.NeoPixel(
    board.D18, NLED, brightness=0.25, pixel_order=neopixel.GRB, auto_write=False)

pixels.fill((0, 0, 0))

i = 0

while(True):

    i += 0.5

    for x in range(NLED):
        y = math.sin((x+i) * 0.20)  # sin(x)
        b = (y + 1) / 2 * 255  # scale
        pixels[x] = (0, int(min(b+50, 255)), int(b))

    pixels.show()
    sleep(0.05)
