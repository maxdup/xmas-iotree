import random
import math
import time

from _runtime import Runtime, NLED, COORDS, BOUNDING_BOX

rt = Runtime()
decay = 4


def distance(p1, p2):
    distX = (COORDS[p1][0] - COORDS[p2][0]) ** 2
    distY = (COORDS[p1][1] - COORDS[p2][1]) ** 2
    distZ = ((COORDS[p1][2] - COORDS[p2][2]) * 2) ** 2
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
        rt[i] = outColor(rt[i], d)

    bombAge = bombAge + 0.05

    if bombAge > 1.5:
        bomb = None

    time.sleep(0.0125)

    rt.show()
