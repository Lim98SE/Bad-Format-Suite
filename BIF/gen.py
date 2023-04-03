from PIL import Image
from math import sqrt
import sys

name = " ".join(sys.argv)

base = Image.open(name)
base_pixels = base.getdata()

print(base.size)

newData = []

COLORS = []

with open("colors.hex") as color_file:
   for i in color_file.read().split("\n"):
       if len(i) == 6:
           h = i.lstrip('#')
           COLORS.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

size_x, size_y = base.width, base.height

for pixel in base_pixels:
    newData.append(closest_color(pixel))

fileOutput = bytearray(size_x.to_bytes(2, "big"))
fileOutput.extend(size_y.to_bytes(2, "big"))

for pixel in newData:
    fileOutput.append(COLORS.index(pixel))

with open("output.bif", "wb") as output_file:
    output_file.write(fileOutput)

print("Wrote to output.bif")
