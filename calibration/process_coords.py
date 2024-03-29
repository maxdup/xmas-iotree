from utils import IOArgParser, JSONFileRead, JSONFileWrite

CAMERA_SPACE = (1080, 1920)  # portrait
# CAMERA_SPACE = (1920, 1080) # landscape


def offset(arrays):
    # for poorly aligned captures
    # offset value by average delta
    arrs_offset = [arr for arr in arrs]
    for i in range(1, len(arrs_offset)):
        deltas = [arrs[0][j] - arrs[i][j] for j in range(len(arrs[i]))]

        offset = sum(deltas) / len(deltas)
        arrs_offset[i] = [x+offset for x in arrs_offset[i]]


def aggregate(arrs):  # arrays to be averaged together

    # average values
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

    args = IOArgParser(
        'Combines scan data into single coords',
        'scanned_coordinates.json',
        'The filename for your scanned coordinates',
        'processed_coordinates.json',
        'The filename for your processed coordinates',
    )

    raw_coords = JSONFileRead(args.input_coords)

    NLED = min(len(raw_coords['xpos']),
               len(raw_coords['ypos']),
               len(raw_coords['xneg']),
               len(raw_coords['yneg']),)

    coords = [(0, 0, 0)] * NLED

    maxW = CAMERA_SPACE[0]  # horizontal offset
    maxH = CAMERA_SPACE[1]

    Xs = aggregate([[p[0]if p else None for p in raw_coords['xpos']],
                    [maxW - p[0] if p else None for p in raw_coords['xneg']]])

    Ys = aggregate([[p[0] if p else None for p in raw_coords['ypos']],
                    [maxW - p[0] if p else None for p in raw_coords['yneg']]])

    Zs = aggregate([[maxH - p[1] if p else None for p in raw_coords['xpos']],
                    [maxH - p[1] if p else None for p in raw_coords['xneg']],

                    [maxH - p[1] if p else None for p in raw_coords['ypos']],
                    [maxH - p[1] if p else None for p in raw_coords['yneg']]])

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

    JSONFileWrite(args.output_coords, coords)
