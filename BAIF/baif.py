from PIL import Image
from math import sqrt
import sys
import cv2
import os
import re

name = "data"
filename = " ".join(sys.argv)
  
# Read the video from specified path
cam = cv2.VideoCapture(filename)
  
try:
     
   # creating a folder named data
   if not os.path.exists(name):
       os.makedirs(name)
 
# if not created then raise error
except OSError:
   print (f'Error: Creating directory of {name}')

currentframe = 0
frames = 6
  
while(True):
     
   # reading from frame
   ret,frame = cam.read()
 
   if ret:
       # if video is still left continue creating images
       filename = f'./{name}/' + str(currentframe) + '.jpg'
       print ('Extracting frame ' + str(currentframe))
 
       # writing the extracted images
       cv2.imwrite(filename, frame)
 
       # increasing counter so that it will
       # show how many frames are created
       currentframe += 1
       frames += 1
   else:
       break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()

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

os.chdir(name)

print("Encoding...")

frame = Image.open("1.jpg")
size_x, size_y = frame.size

fileOutput = bytearray(size_x.to_bytes(2, "big"))
fileOutput.extend(size_y.to_bytes(2, "big"))
fileOutput.extend(frames.to_bytes(8, "big"))

frames = os.listdir()
frames.sort(key=lambda f: int(re.sub('\D', '', f)))

for i in frames:
    print("Encoding", i)

    newData = []
    chunk = bytearray()

    base = Image.open(i)
    base_pixels = base.getdata()

    for pixel in base_pixels:
        newData.append(closest_color(pixel))

    for pixel in newData:
        chunk.append(COLORS.index(pixel))

    fileOutput.extend(chunk)
    fileOutput.extend(b"CHUNK")

    print("Done")

fileOutput.extend(b"END")

with open("output.baif", "wb") as output_file:
    output_file.write(fileOutput)

print("Wrote")
