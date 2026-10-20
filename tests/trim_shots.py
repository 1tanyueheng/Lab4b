"""Trim the captured screenshots down to their actual content."""
import os

from PIL import Image

SHOTS = r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4b\screenshots"

for name in sorted(os.listdir(SHOTS)):
    if not name.endswith(".png"):
        continue
    path = os.path.join(SHOTS, name)
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        # find the last row that is not pure white / not uniform background
        bg = im.getpixel((w - 2, h - 2))
        last = 0
        for y in range(h - 1, -1, -1):
            row = [im.getpixel((x, y)) for x in range(0, w, 3)]
            if any(abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) > 24 for p in row):
                last = y
                break
        if last == 0 or last >= h - 12:
            print(f"  keep  {name} ({w}x{h})")
            continue
        top = max(0, last + 18)
        out = im.crop((0, 0, w, min(h, top)))
        out.save(path, "PNG", optimize=True)
        print(f"  trim  {name}: {w}x{h} -> {out.size[0]}x{out.size[1]}")

print("done")
