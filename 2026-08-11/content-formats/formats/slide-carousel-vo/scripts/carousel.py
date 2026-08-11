#!/usr/bin/env python3
"""Kodak carousel cut (F10): one held slide per point, no zoom push.

On a MAJOR change (the 20 line boundaries) the outgoing slide goes to black for a few frames, then
the incoming slide flicks up from below, overshoots and settles, the way a tray seats a slide. The
other 29 changes are plain hard cuts.

The black sits at the END of the outgoing beat and the flick at the START of the incoming one, so
the new picture lands on the word rather than a fifth of a second after it.

Writes the silent body plus sfx/cues.json (the second each clunk fires). VHS grade, audio mix and
captions all happen after this, in bin_carousel.sh.

Usage: ./bin_carousel.py
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 24
TAIL = 0.45
BLACK_FRAMES = 3          # 0.125s of black before a major change
SLIDE_FRAMES = 5          # the flick up
TRAVEL = 0.25             # how far below the frame the incoming slide starts, as a fraction of H
OVERSHOOT = 2.2           # back-out easing constant; >0 means it goes past and settles back

HERE = Path(__file__).parent


def back_out(p, s=OVERSHOOT):
    p -= 1.0
    return p * p * ((s + 1) * p + s) + 1.0


def load(name):
    im = Image.open(HERE / f"gen/{name}.png").convert("RGB")
    sc = max(W / im.width, H / im.height)
    im = im.resize((max(W, int(im.width * sc + .5)), max(H, int(im.height * sc + .5))), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((l, t, l + W, t + H)), dtype=np.uint8)


def main:
    beats = json.load(open(HERE / "work/beats.json"))
    timeline = json.load(open(HERE / "vo/timeline.json"))
    total = timeline["total"] + TAIL
    nframes = int(round(total * FPS))

    plates = {b["still"]: load(b["still"]) for b in beats}
    starts = [int(round(b["start"] * FPS)) for b in beats]

    # a major is the first beat of a spoken line, flagged when the beat map was built. Matching
    # whisper onsets against the stem starts does not work: they are different measurements.
    major = [i for i, b in enumerate(beats) if b.get("major")]
    cues = [round((starts[i] - BLACK_FRAMES) / FPS, 3) for i in major if i > 0]
    json.dump(cues, open(HERE / "sfx/cues.json", "w"))
    # the hard cuts get their own much quieter tick, fired on the cut itself
    minor = [round(starts[i] / FPS, 3) for i in range(1, len(beats)) if not beats[i].get("major")]
    json.dump(minor, open(HERE / "sfx/cues_minor.json", "w"))

    owner = np.zeros(nframes, dtype=np.int32)
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else nframes
        owner[s:e] = i

    black = set
    slide = {}
    for i in major:
        if i == 0:
            continue
        f = starts[i]
        for k in range(max(0, f - BLACK_FRAMES), f):
            black.add(k)
        for k in range(SLIDE_FRAMES):
            if f + k < nframes:
                slide[f + k] = (k + 1) / SLIDE_FRAMES

    enc = subprocess.Popen(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium",
         "-crf", "17", "-pix_fmt", "yuv420p", str(HERE / "work/carousel_body.mp4")],
        stdin=subprocess.PIPE)

    blank = np.zeros((H, W, 3), dtype=np.uint8)
    for f in range(nframes):
        if f in black:
            enc.stdin.write(blank.tobytes)
            continue
        img = plates[beats[owner[f]]["still"]]
        p = slide.get(f)
        if p is None:
            enc.stdin.write(img.tobytes)
            continue
        # offset > 0 draws the slide lower in frame; back_out overshoots past 0 then settles
        off = int(round(TRAVEL * H * (1.0 - back_out(p))))
        out = blank.copy
        if off > 0:
            keep = H - off
            if keep > 0:
                out[off:, :] = img[:keep, :]
        elif off < 0:
            keep = H + off
            if keep > 0:
                out[:keep, :] = img[-off:, :]
        else:
            out = img
        enc.stdin.write(out.tobytes)

    enc.stdin.close
    if enc.wait != 0:
        raise SystemExit("encode failed")
    print(f"[carousel] work/carousel_body.mp4  {nframes} frames, {len(major)} majors, {len(cues)} clunks, {len(minor)} ticks")


if __name__ == "__main__":
    main
