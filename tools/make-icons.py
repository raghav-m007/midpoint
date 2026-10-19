#!/usr/bin/env python3
"""Generate Midpoint's app icons. Standard library only -- no pip, no network.

The mark: two small end dots on a rule, with a larger filled dot halfway between.
Shapes come from signed distance fields so one sample per pixel is enough.
"""
import math, os, struct, zlib

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
BG     = (0x10, 0x14, 0x1A)
RULE   = (0x2C, 0x36, 0x45)
END    = (0x6B, 0x7C, 0x93)
ACCENT = (0x5B, 0x9D, 0xF9)

clamp = lambda v, lo=0.0, hi=1.0: lo if v < lo else hi if v > hi else v

def over(dst, src, a):
    if a <= 0: return dst
    if a >= 1: return src
    return tuple(int(round(d + (s - d) * a)) for d, s in zip(dst, src))

def render(size, scale=1.0):
    px = 1.0 / size
    cov = lambda sd: clamp(0.5 - sd / px)
    half  = 0.300 * scale          # distance from centre to each end dot
    rule_h = 0.016 * scale
    r_end  = 0.052 * scale
    r_mid  = 0.125 * scale
    ring   = 0.034 * scale         # halo gap around the middle dot

    rows = []
    for y in range(size):
        row = bytearray()
        uy = (y + 0.5) / size - 0.5
        for x in range(size):
            ux = (x + 0.5) / size - 0.5
            c = BG
            # the rule, cut away around the middle dot so the dot reads as separate
            bar = max(abs(ux) - half, abs(uy) - rule_h)
            if bar < px * 2:
                gap = math.hypot(ux, uy) - (r_mid + ring)
                c = over(c, RULE, min(cov(bar), cov(-gap)))
            for ex in (-half, half):
                c = over(c, END, cov(math.hypot(ux - ex, uy) - r_end))
            c = over(c, ACCENT, cov(math.hypot(ux, uy) - r_mid))
            row += bytes(c)
        rows.append(bytes(row))
    return rows

def write_png(path, size, rows):
    raw = b"".join(b"\x00" + r for r in rows)
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    open(path, "wb").write(png)
    return len(png)

def main():
    os.makedirs(OUT, exist_ok=True)
    for name, size, scale in [("icon-192.png", 192, 1.0), ("icon-512.png", 512, 1.0),
                              ("icon-maskable-512.png", 512, 0.72), ("apple-touch-icon.png", 180, 1.0)]:
        print(name, write_png(os.path.join(OUT, name), size, render(size, scale)), "bytes")

if __name__ == "__main__":
    main()
