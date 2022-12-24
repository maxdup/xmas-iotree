import json
import time
import board
import neopixel


with open('/var/www/xmas-iotree/coordinates.json', 'r+') as f:
    coords = json.loads(f.read() or '{}')
    NLED = len(coords)

pixels = neopixel.NeoPixel(
    board.D18, NLED, brightness=0.25, pixel_order=neopixel.GRB, auto_write=False)

pixels.fill((0, 0, 0))


deltaX = 2
deltaY = 2
deltaZ = 2

def toRGBval(dist):
    d = max(0, 0.10 - dist)
    s = min(0.25, d)
    return int(d / 0.25 *255)

percent = 0
lastTime = time.time()

while (True):
    deltaTime = time.time() - lastTime
    lastTime = time.time()

    percent += 10 * deltaTime # 10 percent per second
    percent %= 100

    targetX = -1 + (percent/100) * 2
    targetY = -1 + (percent/100) * 2
    targetZ = -1 + (percent/100) * 2

    for j in range(NLED):

        xdist = abs(coords[j][0] - targetX)
        ydist = abs(coords[j][1] - targetY)
        zdist = abs(coords[j][2] - targetZ)

        pixels[j] = (toRGBval(xdist),
                     toRGBval(ydist),
                     toRGBval(zdist))

    pixels.show()
    time.sleep(0.1)
