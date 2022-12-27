from time import sleep
import math
import json

from _runtime import Runtime, NLED, COORDS, BOUNDING_BOX

rt = Runtime()

rt.fill((0, 0, 0))

i = 0

while(True):

    i += 0.5

    for x in range(NLED):
        y = math.sin((x+i) * 0.20)  # sin(x)
        b = (y + 1) / 2 * 255  # scale
        rt[x] = (int(min(b+50, 255)), 0, int(b))

    rt.show()
    sleep(0.05)
