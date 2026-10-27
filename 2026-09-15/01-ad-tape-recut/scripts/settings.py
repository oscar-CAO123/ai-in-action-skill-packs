"""Frames for the settings map: one at 6 s and one mid-film per source, plus a strip every 12 s.
Writes settings/<prefix>-6s.jpg, settings/<prefix>-mid.jpg, settings/strips.png. Group them by
room and light into SETTINGS.md by eye. Law 3: a recipe never crosses a setting."""
import json, subprocess
from pathlib import Path

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV
OUT = HERE / "settings"; OUT.mkdir(exist_ok=True)

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())

strips = []
for prefix, film in TAPE["films"].items():
    v = next(p for p in SRC.glob(TAPE["glob"]) if p.stem.replace(" ", "") == film["stem"])
    d = dur(v)
    for tag, t in (("6s", 6.0), ("mid", d / 2)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-q:v", "3", str(OUT / f"{prefix}-{tag}.jpg")], check=True)
    strip = OUT / f"_{prefix}-strip.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vf", "fps=1/12,scale=180:-1,tile=12x1", "-frames:v", "1", str(strip)], check=True)
    strips.append(strip)
    print(prefix, f"{d:.0f}s", flush=True)
if strips:
    args = ["ffmpeg", "-v", "error", "-y"]
    for s in strips: args += ["-i", str(s)]
    args += ["-filter_complex", "".join(f"[{i}:v]" for i in range(len(strips))) + f"vstack=inputs={len(strips)}", str(OUT / "strips.png")]
    subprocess.run(args, check=True)
print("done; write SETTINGS.md from the frames")
