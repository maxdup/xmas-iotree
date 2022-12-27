import time
from _runtime import Runtime, NLED, COORDS, BOUNDING_BOX

rt = Runtime()

for i in range(NLED):
    rt[i] = (0, 0, 0)

rt.show()


while(True):
    for i in range(len(rt)):
        rt[i] = ((rt[i][0] + 1) % 255,
                 (rt[i][1] + 1) % 255,
                 (rt[i][2] + 1) % 255)

    rt.show()
    time.sleep(0.1)
