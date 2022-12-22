import os
import sys
import inspect
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import NLED

COORD_INPUT_FILE = 'raw_coordinates.json'
COORD_OUTPUT_FILE = 'coordinates.json'


def aggregate(arrs): # arrays to be averaged together

    # offset value by average delta
    arrs_offset = [arr for arr in arrs]
    for i in range(1, len(arrs_offset)):
        deltas = [arrs[0][j] - arrs[i][j] for j in range(len(arrs[i]))]
        offset = sum(deltas) / len(deltas)
        arrs_offset[i] = [x+offset for x in arrs_offset[i]]

    # average offset values
    coords = []
    for i in range(0, len(arrs_offset[0])):
        vals = [arrs_offset[j][i] for j in range(len(arrs_offset))]
        coords.append(sum(vals) / len(vals))
    return coords


if __name__ == '__main__':

    with open(COORD_INPUT_FILE, 'r+') as f:
        content = f.read() or '{}'
        raw_coords = json.loads(content)

    coords = [(0,0,0)] * NLED

    Xs = aggregate([[p[0] for p in raw_coords['xpos']],
                    [p[0]*-1 for p in raw_coords['xneg']]])

    Ys = aggregate([[p[0] for p in raw_coords['ypos']],
                    [p[0]*-1 for p in raw_coords['yneg']]])

    Zs = aggregate([[p[1]*-1 for p in raw_coords['xpos']],
                    [p[1]*-1 for p in raw_coords['xneg']],

                    [p[1]*-1 for p in raw_coords['ypos']],
                    [p[1]*-1 for p in raw_coords['yneg']]])

    coords = [(Xs[i], Ys[i], Zs[i]) for i in range(NLED)]
    print(coords)
