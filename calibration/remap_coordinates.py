import json

COORD_INPUT_FILE = 'corrected_coordinates.json'
COORD_OUTPUT_FILE = 'coordinates.json'

CAMERA_SPACE = (1080, 1920) # portrait
# CAMERA_SPACE = (1920, 1080) # landscape

with open(COORD_INPUT_FILE, 'r+') as f:
    content = f.read() or '{}'
    coords = json.loads(content)

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
                     (c[2] - minZ) / deltaZ ])

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

print(scaled)

with open(COORD_OUTPUT_FILE, 'w') as f:
    output = json.dumps(scaled)
    f.write(output)
