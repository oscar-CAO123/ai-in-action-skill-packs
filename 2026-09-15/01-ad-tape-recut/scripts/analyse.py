"""Per source film: silence gaps (audio) and caption-band change frames (vision).
Writes analysis/<stem>.json. The caption band is the strip of the frame the burned-in captions
sit in; measure it once on one film and set caption_band in tape.json as [w, h, x, y] in source
pixels (default is the lower third of a 720x1280 frame)."""
import json, re, subprocess
from pathlib import Path

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV
OUT = HERE / "analysis"; OUT.mkdir(exist_ok=True)
W, H, X, Y = TAPE.get("caption_band", [720, 320, 0, 860])

def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr

for v in sorted(SRC.glob(TAPE["glob"])):
    stem = v.stem.replace(" ", "")
    err = run(["ffmpeg", "-v", "info", "-i", str(v), "-af", "silencedetect=n=-32dB:d=0.12", "-vn", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    err = run(["ffmpeg", "-v", "info", "-i", str(v), "-vf", f"crop={W}:{H}:{X}:{Y},select='gt(scene,0.05)',showinfo", "-an", "-f", "null", "-"])
    caps = [round(float(x), 3) for x in re.findall(r"pts_time:([\d.]+)", err)]
    json.dump({"silence": list(zip(starts, ends)), "caption_changes": caps}, open(OUT / f"{stem}.json", "w"))
    print(stem, "silences", len(starts), "caption changes", len(caps), flush=True)
