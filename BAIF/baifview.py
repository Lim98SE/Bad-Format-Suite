# ABIF VIEWER
import pygame
import sys

filename = " ".join(sys.argv)

print("Loading file...")

with open(filename, "rb") as input_file:
    data = input_file.read()

COLORS = []

with open("colors.hex") as color_file:
   for i in color_file.read().split("\n"):
       if len(i) == 6:
           h = i.lstrip('#')
           COLORS.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

size_x, size_y, frame_count = int.from_bytes(data[0:2]), int.from_bytes(data[2:4]), int.from_bytes(data[4:12])
print(size_x, size_y, frame_count)

data = data[12:]

frame_data = data.split(b"CHUNK")
frames = []

print(len(frames))

frame = 0

# decode frames into bytes
for i in frame_data:
    current_frame = bytearray()

    if i == b"END": break

    print("Loading frame", frame)
    frame += 1

    for p in i:
        pixel = COLORS[int(p)]
        current_frame.extend(bytes(pixel))
    
    frames.append(
        pygame.image.frombytes(bytes(current_frame), (size_x, size_y), "RGB")
        )

window = pygame.display.set_mode((size_x, size_y), pygame.NOFRAME)

clock = pygame.time.Clock()

for i in frames:
    pygame.event.get()
    window.blit(i, (0, 0))
    pygame.display.update()
    clock.tick(24)
