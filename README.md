# Bad Format Suite
## A repo for my Bad File Formats (BIF, and whatever else I make)

## BIF (Bad Image Format)
### Bytes
Byte 00 and 01: Width

Byte 02 and 03: Height

Bytes 04 and on: Color index (one byte per pixel)

## BAIF (Bad Animated Image Format)
### Bytes

Same header as BIF with one addition

Bytes 04 to 12: Number of frames (32 bit integer)

Bytes 13 and on: each frame

Each frame is seperated by 5 bytes reading **CHUNK**. The end of the file is marked by **CHUNKEND**.
