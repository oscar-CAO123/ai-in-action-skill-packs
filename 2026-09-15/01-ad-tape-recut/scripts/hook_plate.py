"""The cut plus the text hook. A white plate covers the burned-in card's exact box (no blur) with
the two hook lines inside it; a film with no card gets the pill pair at the top; a hook with "y"
is placed there. Usage: hook_plate.py [ids] -> hooked/<id>.mp4. Reads hooks.json, cuts/<id>.timeline.json,
analysis/_cardbox.json."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
HOOKS = {k: v for k, v in json.load(open(HERE / "hooks.json")).items() if not k.startswith("_")}
CARDS = json.load(open(HERE / "analysis" / "_cardbox.json")) if (HERE / "analysis" / "_cardbox.json").exists() else {}
OUT = HERE / "hooked"; OUT.mkdir(exist_ok=True)
FW, FH = 1080, 1920
SRC_W = TAPE.get("output", [720, 1280, 30])[0]; S = FW / SRC_W
FONT = TAPE.get("hook_font")   # ENV: a .ttf path; the brand's heavy face if it has one
CANDIDATES = [FONT, "/System/Library/Fonts/SFCompact.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"]
FONT = next((f for f in CANDIDATES if f and Path(f).exists()), None)
def font(size): return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()

def plate_png(text, card, path):
    im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = card["x0"] * S - 6, card["y0"] * S - 6, card["x1"] * S + 6, card["y1"] * S + 6
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=(255, 255, 255, 255))
    lines = text.split("\n"); size = 58
    while size > 30:
        f = font(size); lh = size * 1.15
        if max(d.textlength(l, font=f) for l in lines) <= (x1 - x0) - 60 and lh * len(lines) <= (y1 - y0) - 24: break
        size -= 2
    cy = (y0 + y1) / 2; top = cy - lh * len(lines) / 2
    for i, l in enumerate(lines): d.text(((x0 + x1) / 2, top + lh * i + lh / 2), l, font=f, fill=(0, 0, 0, 255), anchor="mm")
    im.save(path)

def pills_png(text, y, path):
    im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = font(56); lh = 78; cy = y if y else 330
    for i, l in enumerate(text.split("\n")):
        tw = d.textlength(l, font=f); yy = cy + i * lh
        d.rounded_rectangle([FW / 2 - tw / 2 - 28, yy - 36, FW / 2 + tw / 2 + 28, yy + 36], radius=18, fill=(255, 255, 255, 255))
        d.text((FW / 2, yy), l, font=f, fill=(0, 0, 0, 255), anchor="mm")
    im.save(path)

ids = sys.argv[1:] or list(HOOKS)
for rid in ids:
    tl = json.load(open(HERE / "cuts" / f"{rid}.timeline.json"))
    first_film = tl["parts"][0]["film"]; card = CARDS.get(TAPE["films"][first_film]["stem"])
    png = OUT / f"_{rid}-hook.png"
    if "y" in HOOKS[rid]: pills_png(HOOKS[rid]["text_hook"], HOOKS[rid]["y"], png)
    elif card: plate_png(HOOKS[rid]["text_hook"], card, png)
    else: pills_png(HOOKS[rid]["text_hook"], None, png)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(HERE / "cuts" / f"{rid}.mp4"), "-loop", "1", "-i", str(png),
                    "-filter_complex", f"[0:v]scale={FW}:{FH}:flags=lanczos[b];[b][1:v]overlay=0:0:shortest=1[v]",
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", str(OUT / f"{rid}.mp4")], check=True)
    print(rid, "->", f"hooked/{rid}.mp4", flush=True)
