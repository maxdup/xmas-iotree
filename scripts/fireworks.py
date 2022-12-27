import neopixel
import board
import json
import random
import math
import time

with open('/var/www/xmas-iotree/coordinates.json', 'r+') as f:
    coords = json.loads(f.read() or '{}')
    NLED = len(coords)

pixels = neopixel.NeoPixel(
    board.D18, NLED, brightness=0.25, pixel_order=neopixel.GRB, auto_write=False)


pixels.fill((0, 0, 0))

decay = 4


def distance(p1, p2):
    distX = (coords[p1][0] - coords[p2][0]) ** 2
    distY = (coords[p1][1] - coords[p2][1]) ** 2
    distZ = ((coords[p1][2] - coords[p2][2]) * 2) ** 2
    return abs(math.sqrt(distX + distY + distZ))


def outColor(initialColor, dist):
    if dist <= bombAge + 0.1 and dist > bombAge:
        return (255, 255, 255)
    if dist < bombAge:
        return bombColor
    else:
        return (max(0, initialColor[0] - decay),
                max(0, initialColor[1] - decay),
                max(0, initialColor[2] - decay))


bombAge = 0
bomb = None

while(True):
    if not bomb:
        bomb = random.randint(0, NLED-1)
        bombColor = (random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255))
        bombAge = 0

    for i in range(NLED):
        d = distance(bomb, i)
        pixels[i] = outColor(pixels[i], d)

    bombAge = bombAge + 0.05

    if bombAge > 1.5:
        bomb = None

    time.sleep(0.0125)

    pixels.show()
