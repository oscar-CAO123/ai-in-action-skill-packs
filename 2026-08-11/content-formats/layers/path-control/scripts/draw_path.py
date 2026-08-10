#!/usr/bin/env python3
"""Draw a camera-path annotation on a plate, to the measured L-PATH spec.

    python3 draw_path.py plate.png out.png --waypoints 0.82,0.74 0.55,0.38 0.18,0.62

Waypoints are fractions of width,height in camera order. The stroke is a smooth
spline through them at 1.25% of frame width in #E4192A, numbered 1..n.
Same waypoints on two plates give the identical move, which is what F15 needs.
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

RED = (228, 25, 42)          # midpoint of the measured #E01925 to #E91B28 band
STROKE_PCT = 0.0125          # measured 1.1% to 1.4% of frame width
LABEL_PCT = 0.045            # numeral cap height as a fraction of frame width

FONTS = ["/System/Library/Fonts/Supplemental/Futura.ttc",
         "/System/Library/Fonts/Helvetica.ttc",
         "/Library/Fonts/Arial Bold.ttf"]


def catmull_rom(pts, samples=40):
    """Smooth curve through every point, so the drawn route reads as one hand stroke."""
    if len(pts) < 3:
        return pts
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i:i + 4]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    out.append(pts[-1])
    return out


def load_font(size):
    for f in FONTS:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plate")
    ap.add_argument("out")
    ap.add_argument("--waypoints", nargs="+", required=True,
                    help="x,y fractions in camera order, e.g. 0.8,0.7 0.5,0.4")
    ap.add_argument("--width-pct", type=float, default=STROKE_PCT)
    ap.add_argument("--no-labels", action="store_true")
    a = ap.parse_args()

    im = Image.open(a.plate).convert("RGB")
    W, H = im.size
    pts = []
    for w in a.waypoints:
        x, y = (float(v) for v in w.split(","))
        pts.append((x * W, y * H))
    if len(pts) < 2:
        raise SystemExit("need at least two waypoints")

    sw = max(2, round(a.width_pct * W))
    d = ImageDraw.Draw(im)
    curve = catmull_rom(pts)
    d.line(curve, fill=RED, width=sw, joint="curve")
    for x, y in curve:                                   # round the caps and joins
        d.ellipse([x - sw / 2, y - sw / 2, x + sw / 2, y + sw / 2], fill=RED)

    if not a.no_labels:
        font = load_font(round(LABEL_PCT * W))
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        off = sw * 3.2
        for i, (x, y) in enumerate(pts, 1):
            # sit the numeral off the side of the stroke, never on it
            j = min(range(len(curve)), key=lambda k: (curve[k][0] - x) ** 2 + (curve[k][1] - y) ** 2)
            ax, ay = curve[max(j - 3, 0)]
            bx, by = curve[min(j + 3, len(curve) - 1)]
            tx, ty = bx - ax, by - ay
            n = (tx * tx + ty * ty) ** 0.5 or 1.0
            nx, ny = -ty / n, tx / n
            if (x + nx * off - cx) ** 2 + (y + ny * off - cy) ** 2 < \
               (x - nx * off - cx) ** 2 + (y - ny * off - cy) ** 2:
                nx, ny = -nx, -ny          # push away from the path, not into it
            d.text((x + nx * off, y + ny * off), str(i), font=font, fill=RED, anchor="mm")

    im.save(a.out)
    print(f"{a.out}  {W}x{H}  stroke {sw}px ({100 * sw / W:.2f}% of width)  "
          f"{len(pts)} waypoints")


if __name__ == "__main__":
    main()
