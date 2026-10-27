"""Find the burned-in headline card's box once per film: analysis/_cardbox.json as
{stem: {x0, y0, x1, y1, t}} in source pixels. Looks for the largest near-white rectangle in the
top 60 percent of a frame at t seconds (default 5). Check the boxes by eye on the settings frames;
a film with no card gets no entry and the hook step falls back to the pill pair."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV
OUT = HERE / "analysis"; OUT.mkdir(exist_ok=True)
T = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
boxes = {}
for prefix, film in TAPE["films"].items():
    v = next(p for p in SRC.glob(TAPE["glob"]) if p.stem.replace(" ", "") == film["stem"])
    png = OUT / f"_{prefix}-card.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{T}", "-i", str(v), "-frames:v", "1", str(png)], check=True)
    im = Image.open(png).convert("L"); w, h = im.size; px = im.load()
    rows = [sum(1 for x in range(w) if px[x, y] > 235) for y in range(int(h * 0.6))]
    ys = [y for y, n in enumerate(rows) if n > w * 0.45]
    if not ys: print(prefix, "no card found"); continue
    y0, y1 = ys[0], ys[-1]
    cols = [sum(1 for y in range(y0, y1 + 1) if px[x, y] > 235) for x in range(w)]
    xs = [x for x, n in enumerate(cols) if n > (y1 - y0) * 0.6]
    boxes[film["stem"]] = {"x0": xs[0], "y0": y0, "x1": xs[-1], "y1": y1, "t": T}
    print(prefix, boxes[film["stem"]])
json.dump(boxes, open(OUT / "_cardbox.json", "w"), indent=1)
