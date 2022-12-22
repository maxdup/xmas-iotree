import os
import sys
import inspect
import json
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import NLED  # NOQA: #E402


COORD_INPUT_FILE = 'raw_coordinates.json'
COORD_OUTPUT_FILE = 'coordinates.json'


def offset(arrays):
    # for poorly aligned captures
    # offset value by average delta
    arrs_offset = [arr for arr in arrs]
    for i in range(1, len(arrs_offset)):
        deltas = [arrs[0][j] - arrs[i][j] for j in range(len(arrs[i]))]

        offset = sum(deltas) / len(deltas)
        arrs_offset[i] = [x+offset for x in arrs_offset[i]]


def aggregate(arrs):  # arrays to be averaged together

    # arrso = offset(arrs)

    # average offset values
    coords = []
    for i in range(0, len(arrs[0])):
        vals = [arrs[j][i] for j in range(len(arrs))]
        vals = [abs(x) for x in vals if x]
        if vals:
            coords.append(sum(vals) / len(vals))
        else:
            coords.append(None)
    return coords


if __name__ == '__main__':

    with open(COORD_INPUT_FILE, 'r+') as f:
        content = f.read() or '{}'
        raw_coords = json.loads(content)

    coords = [(0, 0, 0)] * NLED

    Xs = aggregate([[p[0] if p else None for p in raw_coords['xpos']],
                    [p[0]*-1 if p else None for p in raw_coords['xneg']]])

    Ys = aggregate([[p[0] if p else None for p in raw_coords['ypos']],
                    [p[0]*-1 if p else None for p in raw_coords['yneg']]])

    Zs = aggregate([[p[1]*-1 if p else None for p in raw_coords['xpos']],
                    [p[1]*-1 if p else None for p in raw_coords['xneg']],

                    [p[1]*-1 if p else None for p in raw_coords['ypos']],
                    [p[1]*-1 if p else None for p in raw_coords['yneg']]])

    coords = [(Xs[i], Ys[i], Zs[i]) for i in range(NLED)]

    def avg(pos, val, prv, nxt):
        # todo improve
        if pos == 0:
            return (prv[0], val[1], val[2])
        if pos == 1:
            return (val[0], prv[1], val[2])
        if pos == 2:
            return (val[0], val[1], prv[2])

    for i in range(len(coords)):
        if not coords[i][0]:
            coords[i] = avg(0, coords[i], coords[i-1], coords[i+1])
        if not coords[i][1]:
            coords[i] = avg(1, coords[i], coords[i-1], coords[i+1])
        if not coords[i][2]:
            coords[i] = avg(2, coords[i], coords[i-1], coords[i+1])

    for c in coords:
        if not c[0] or not c[1] or not c[2]:
            print(c)

    output = json.dumps(coords)

    with open(COORD_OUTPUT_FILE, 'w') as f:
        f.write(output)
