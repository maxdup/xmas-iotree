import os
import time
import json

NLED = 0
COORDS = []

dataDir = os.path.join(os.path.dirname(__file__), '..')
dataDir = os.path.join(dataDir, 'data')

isPI = os.uname()[4][:3] == 'arm'

try:
    with open(os.path.join(dataDir, 'coordinates.json'), 'r+') as f:
        DATA = json.loads(f.read() or '{}')
        COORDS = DATA['coords']
        BOUNDING_BOX = DATA['bounding_box']
        NLED = len(COORDS)
except Exception as e:
    print('Could not find coordinates, see /data/pull_coords.py')

try:
    import board
    import neopixel
except ImportError:
    if isPI:
        print('[❌] import error for neopixel')


class Runtime:

    def __init__(self):
        if isPI:
            self._np = neopixel.NeoPixel(
                board.D18, NLED, brightness=0.25,
                pixel_order=neopixel.RGB, auto_write=False)

        self._arr = [[0, 0, 0]] * NLED
        self._lastTime = time.time()

    def show(self):
        # Send a frame

        if isPI:
            self._np.show()

    def time_delta(self):
        # Get time between calls
        delta = time.time() - self._lastTime
        self._lastTime = time.time()
        return delta

    def fill(self, color):
        # Fill every pixel
        if isPI:
            self._np.fill(color)
        else:
            assert len(color) == 3
            for i in color:
                assert isinstance(color[i], int)

    def __len__(self):
        # Get length of leds
        return NLED

    def __getitem__(self, key):
        # Get color at
        if isinstance(key, int) and \
                key in range(NLED):
            return self._arr[key]

    def __setitem__(self, key, value):
        # Set color at
        if isinstance(key, int) and \
                key in range(NLED):
            self._arr[key] = value
            self._np[key] = value
