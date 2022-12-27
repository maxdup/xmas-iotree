import neopixels
import board
import json


with open('/var/www/xmas-iotree/coordinates.json', 'r+') as f:
    coords = json.loads(f.read() or '{}')
    NLED = len(coords)

pixels = neopixel.NeoPixel(
    board.D18, NLED, brightness=0.25, pixel_order=neopixel.GRB, auto_write=False)

for i in range(NLED):
    pixels[i] = (0,0,0)

pixels.show()
