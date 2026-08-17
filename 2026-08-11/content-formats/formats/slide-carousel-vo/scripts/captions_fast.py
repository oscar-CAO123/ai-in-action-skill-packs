#!/usr/bin/env python3
"""Fast caption burn for a slide-carousel film (F10). The LOOK is the canonical house template, unchanged:
Poppins Regular 92px on 1080x1920, pure white, no outline, no shadow, dead centre, one word at a
time, hard cut on the next word's onset, end card left caption-free.

Why not engine/tools/captions/burn_captions.py: it opens one looped PNG input per word and chains
one overlay filter per word. At the ~80 words it was built for that is fine. A slide-carousel film
runs 230+, so ffmpeg gets 230+ input streams and as many chained overlays, and effectively stalls.
Same locked look here, composited per frame through a pipe instead.

Usage: ./bin_captions.py <base.mp4> <words.json> <out.mp4> [--offset 0] [--endclean 3.0]
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 24
def _find_font():
    """Walk up from this script until the engine's captions fonts turn up, so the rig works
    wherever the project folder sits."""
    here = Path(__file__).resolve()
    for parent in [Path.cwd().resolve()] + list(here.parents):
        f = parent / "engine/tools/captions/fonts/Poppins-Regular.ttf"
        if f.exists():
            return f
        f = parent / "../../engine/tools/captions/fonts/Poppins-Regular.ttf"
        if f.exists():
            return f.resolve()
    raise SystemExit("Poppins-Regular.ttf not found; is the engine tools folder reachable?")


FONT = _find_font()
SIZE = 92


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def clean(t):
    return t.strip().rstrip(".,")            # keep ? and !


def main():
    base, words_json, out = sys.argv[1], sys.argv[2], sys.argv[3]
    offset = float(arg("--offset", "0"))
    endclean = float(arg("--endclean", "3.0"))
    total = dur(base)
    endcard_cut = total - endclean

    raw = json.load(open(words_json))
    # Keep zero-duration words. Whisper hands back a start==end span for a word it ran straight
    # through ("Boards" at 12.18), and dropping those silently deletes them from the captions. Each
    # word shows until the NEXT word's onset anyway, so a zero-duration span still renders. Only a
    # zero-duration repeat of the previous word is a real whisper artifact worth dropping.
    words = []
    for w in raw:
        if not clean(w[2]):
            continue
        if w[1] <= w[0] and words and clean(words[-1][2]).lower() == clean(w[2]).lower():
            continue
        words.append(w)

    font = ImageFont.truetype(str(FONT), SIZE)
    ascent, descent = font.getmetrics()
    ch = ascent + descent

    # one sprite per distinct word, and the frame range it owns
    sprites, spans = {}, []
    for i, (st, en, tx) in enumerate(words):
        s = st + offset
        e = (words[i + 1][0] + offset) if i + 1 < len(words) else (en + offset + 0.4)
        if s >= endcard_cut:
            continue
        e = min(e, endcard_cut)
        if e <= s:
            continue
        word = clean(tx)
        if word not in sprites:
            wpx = int(font.getlength(word))
            img = Image.new("RGBA", (wpx, ch), (0, 0, 0, 0))
            ImageDraw.Draw(img).text((0, 0), word, font=font, fill=(255, 255, 255, 255))
            a = np.asarray(img, dtype=np.float32) / 255.0
            sprites[word] = (a[..., :3], a[..., 3:4])
        spans.append((int(round(s * FPS)), int(round(e * FPS)), word))

    per_frame = {}
    for f0, f1, word in spans:
        for f in range(f0, f1):
            per_frame[f] = word

    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", base,
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-r", str(FPS), "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", base, "-map", "0:v", "-map", "1:a?",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", out],
                           stdin=subprocess.PIPE)

    fsz = W * H * 3
    n = 0
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            break
        word = per_frame.get(n)
        if word is None:
            enc.stdin.write(buf)
        else:
            frame = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3).astype(np.float32) / 255.0
            rgb, alpha = sprites[word]
            sh, sw = rgb.shape[:2]
            x0, y0 = (W - sw) // 2, (H - sh) // 2
            patch = frame[y0:y0 + sh, x0:x0 + sw]
            frame[y0:y0 + sh, x0:x0 + sw] = patch * (1 - alpha) + rgb * alpha
            enc.stdin.write((np.clip(frame, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        n += 1

    enc.stdin.close()
    dec.wait()
    if enc.wait() != 0:
        sys.exit("encode failed")
    print(f"WROTE {out}  ({len(spans)} words over {n} frames, {len(sprites)} sprites)")


if __name__ == "__main__":
    main()
