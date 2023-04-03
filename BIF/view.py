from PIL import Image
import sys

name = " ".join(sys.argv)

COLORS = []

with open("colors.hex") as color_file:
   for i in color_file.read().split("\n"):
       if len(i) == 6:
           h = i.lstrip('#')
           COLORS.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

with open(name, "rb") as in_file:
    data = in_file.read()

size_x, size_y = int.from_bytes(data[0:2]), int.from_bytes(data[2:4])
print(size_x, size_y)

data = data[4:]

output = Image.new("RGB", (size_x, size_y))
final_data = []

for i in data:
    final_data.append(COLORS[i])


output.putdata(final_data)
output.show()
