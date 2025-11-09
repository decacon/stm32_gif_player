#!/usr/bin/env python

from PIL import Image
import sys
import os

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <image-file>")
    sys.exit(1)

fname = sys.argv[1]

try:
    img = Image.open(fname)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    if img.width != 160 or img.height != 128:
        print("Error: 160x128 image expected")
        print(f"Actual size: {img.width}x{img.height}")
        sys.exit(2)

    print("const uint16_t test_img_160x128[][160] = {")

    for y in range(img.height):
        row = []
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            color565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
            color565 = ((color565 & 0xFF00) >> 8) | ((color565 & 0xFF) << 8)
            row.append(f"0x{color565:04X}")
        print("  {" + ", ".join(row) + "},")

    print("};")

except FileNotFoundError:
    print(f"Error: File '{fname}' not found")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)