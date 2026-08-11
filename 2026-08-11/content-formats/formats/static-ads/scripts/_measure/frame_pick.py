#!/usr/bin/env python3
"""Turn any clip into founder plates. Contact sheet first, then full-res picks by timestamp.

    python3 _measure/frame_pick.py <video>                  # labelled contact sheet, every 6s
    python3 _measure/frame_pick.py <video> --every 3        # denser sheet
    python3 _measure/frame_pick.py <video> --at 42,66,120   # full-res frames at those seconds
    python3 _measure/frame_pick.py <video> --at 66 --name simon-podcast-composed

Free, every time. Nothing here spends a credit.

## Why the sheet labels its tiles

The first pass of this was an unlabelled ffmpeg `tile` filter, and the tile-to-timestamp mapping
was read off by counting, which was wrong by one tile because the first sample does not land at
t=0. Every tile now carries its own second burned into the corner, so a pick is read straight off
the sheet rather than counted.

## What makes a usable founder plate

Mid-sentence, mouth open on a vowel, eyes to camera, hands in frame if they are moving. Reject
anything caught on a consonant (the mouth pulls flat and reads as a grimace) and anything where
the subject is looking down. Shoot for a matched PAIR when the card is a split screen: same set,
same shirt, same camera, one composed and one animated. That is what makes a seam read as one
person changing register instead of two photographs.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT.parent / "assets" / "founders"


def probe(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,duration", "-of", "csv=p=0", str(video)],
                       capture_output=True, text=True, check=True)
    w, h, d = r.stdout.strip.split(",")[:3]
    return int(w), int(h), float(d)


def sheet(video, every, dst):
    from PIL import Image, ImageDraw, ImageFont
    w, h, dur = probe(video)
    times = list(range(0, int(dur), every))
    tw = 400
    th = round(tw * h / w)
    cols = 6
    rows = (len(times) + cols - 1) // cols
    grid = Image.new("RGB", (tw * cols, th * rows), "black")
    font = ImageFont.truetype(str(ROOT.parent / "assets" / "your display typeface-Bold.ttf"), 26)

    tmp = Path(dst).parent / "_f.png"
    for n, t in enumerate(times):
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", str(tmp), "-y"], check=True)
        if not tmp.exists:
            continue
        im = Image.open(tmp).convert("RGB").resize((tw, th), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        label = f"{t}s"
        d.rectangle((0, th - 36, 74, th), fill="black")
        d.text((8, th - 33), label, font=font, fill="white")
        grid.paste(im, ((n % cols) * tw, (n // cols) * th))
    tmp.unlink(missing_ok=True)
    grid.save(dst)
    return dst, len(times), dur


def pick(video, seconds, name):
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for t in seconds:
        stem = name if name and len(seconds) == 1 else f"{name or Path(video).stem}-{t}s"
        dst = OUT / f"{stem}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", str(dst), "-y"], check=True)
        written.append(dst)
    return written


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        sys.exit(__doc__)
    video = Path(argv[0])
    if not video.exists:
        sys.exit(f"no such file: {video}")

    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    name = opt("--name")
    if "--at" in argv:
        secs = [int(s) for s in opt("--at").split(",")]
        for p in pick(video, secs, name):
            print(f"  {p}")
    else:
        every = int(opt("--every", "6"))
        dst = video.parent / f"{video.stem}-sheet.png"
        dst, n, dur = sheet(video, every, dst)
        print(f"  {n} tiles across {dur:.0f}s -> {dst}")
        subprocess.run(["open", "-a", "Preview", str(dst)])
