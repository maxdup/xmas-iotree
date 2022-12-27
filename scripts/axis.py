import time

from _runtime import Runtime, NLED, COORDS, BOUNDING_BOX

rt = Runtime()


def toRGBval(dist):
    d = max(0, 0.10 - dist)
    s = min(0.25, d)
    return int(d / 0.25 * 255)


percent = 0
lastTime = time.time()

while (True):
    dt = rt.time_delta()

    percent += 10 * dt  # 10 percent per second
    percent %= 100

    targetX = -1 + (percent/100) * 2
    targetY = -1 + (percent/100) * 2
    targetZ = -1 + (percent/100) * 2

    for j in range(NLED):

        xdist = abs(COORDS[j][0] - targetX)
        ydist = abs(COORDS[j][1] - targetY)
        zdist = abs(COORDS[j][2] - targetZ)

        rt[j] = (toRGBval(xdist),
                 toRGBval(ydist),
                 toRGBval(zdist))

    rt.show()
    time.sleep(0.1)
