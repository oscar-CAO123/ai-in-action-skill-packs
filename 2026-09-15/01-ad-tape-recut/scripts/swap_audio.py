"""Mux an enhanced audio file onto a cut with the video stream copied. The raw cut is kept in
cuts/raw-audio/. Usage: swap_audio.py <id> <clean.wav> [<id> <clean.wav> ...]"""
import shutil, subprocess, sys
from pathlib import Path

HERE = Path.cwd(); CUTS = HERE / "cuts"; RAW = CUTS / "raw-audio"; RAW.mkdir(exist_ok=True)
pairs = list(zip(sys.argv[1::2], sys.argv[2::2]))
for rid, wav in pairs:
    cut = CUTS / f"{rid}.mp4"; keep = RAW / f"{rid}.mp4"
    if not keep.exists(): shutil.copy2(cut, keep)
    tmp = CUTS / f"_{rid}.tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(keep), "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(cut); print(rid, "audio swapped, raw kept in cuts/raw-audio/")
