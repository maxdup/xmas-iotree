from utils import IOArgParser, JSONFileRead, JSONFileWrite

CAMERA_SPACE = (1080, 1920)  # portrait
# CAMERA_SPACE = (1920, 1080) # landscape

if __name__ == '__main__':

    args = IOArgParser(
        'Remap coordinates to fill coordinate space',
        'corrected_coordinates.json',
        'The filename for your corrected coordinates',
        'coordinates.json',
        'The filename for your final coordinates')

    coords = JSONFileRead(args.input_coords)

    remapped = []

    # center cam space X,Y
    centered = []
    c_w = CAMERA_SPACE[0] / 2
    c_h = CAMERA_SPACE[1] / 2

    minZ = min([abs(c[2]) for c in coords])
    maxZ = max([abs(c[2]) for c in coords])
    deltaZ = maxZ - minZ

    for c in coords:
        centered.append([c[0] - c_w,
                         c[1] - c_w,
                         (c[2] - minZ) / deltaZ])

    # scale cam space
    absMaxX = max([abs(c[0]) for c in centered])
    absMaxY = max([abs(c[1]) for c in centered])
    absMaxW = max(absMaxX, absMaxY)

    scaled = []
    for c in centered:
        scaled.append([
            c[0] / absMaxW,
            c[1] / absMaxW,
            c[2] * 2 - 1])

    JSONFileWrite(args.output_coords, scaled)
