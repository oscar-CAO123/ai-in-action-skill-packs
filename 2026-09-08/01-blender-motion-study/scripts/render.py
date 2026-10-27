#!/usr/bin/env python3
"""Render one scene JSON headless in Blender: a still PNG or an mp4 out.

    python3 render.py <scene.json> [--out DIR] [--still] [--ratio 9:16] [--scale 0.35] [--seconds N]
    python3 render.py --list-ratios

Finds Blender (the BLENDER env var, then the usual install location for your OS, then PATH),
resolves the ratio to pixel dimensions, resolves relative file paths against the scene file,
resolves `"font": "SomeFont-Regular"` to an installed TTF, then runs Blender in the background
with bpy_scene.py. A sequence is a PNG run muxed with ffmpeg (libx264, yuv420p); a still is one
PNG. Every render writes render.json beside the output with the resolved spec, the Blender
version, the frame count and the wall time. Free and local: this file never calls a paid model.

Importable: render_scene(spec: dict, out_dir: Path, base: Path | None = None) -> Path
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

HERE = Path(__file__).resolve().parent
BPY = HERE / "bpy_scene.py"

RATIOS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "4:5": (1080, 1350), "1:1": (1080, 1080)}

# Where fonts live, per OS. Add your own directory to FONT_DIRS if yours is elsewhere.
_HOME = Path.home()
FONT_DIRS = {
    "Darwin": [_HOME / "Library" / "Fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts")],
    "Linux": [_HOME / ".fonts", _HOME / ".local" / "share" / "fonts", Path("/usr/share/fonts"), Path("/usr/local/share/fonts")],
    "Windows": [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
                Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"],
}.get(platform.system(), [])

# Where Blender usually is, per OS. The BLENDER environment variable wins over all of these.
_BLENDER_CANDIDATES = {
    "Darwin": ["/Applications/Blender.app/Contents/MacOS/Blender", "/opt/homebrew/bin/blender", "/usr/local/bin/blender"],
    "Linux": ["/usr/bin/blender", "/snap/bin/blender", "/usr/local/bin/blender", str(_HOME / "blender" / "blender")],
    "Windows": [str(Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Blender Foundation" / d / "blender.exe")
                for d in ("Blender 5.2", "Blender 5.1", "Blender 5.0", "Blender 4.5")],
}.get(platform.system(), [])


def blender_bin() -> str:
    env = os.environ.get("BLENDER")
    if env and (shutil.which(env) or Path(env).exists()):
        return env
    for c in _BLENDER_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("blender")
    if found:
        return found
    raise SystemExit("Blender not found. Install Blender 5.2 LTS from blender.org, then either put it on PATH "
                     "or set BLENDER=/full/path/to/the/blender/executable.")


def ratio_dims(ratio: str) -> tuple[int, int]:
    if ratio in RATIOS:
        return RATIOS[ratio]
    raise SystemExit(f"unknown ratio {ratio!r}; one of {', '.join(RATIOS)}")


def font_path(name: str) -> str:
    """'Inter-Regular' -> the installed TTF/OTF. An absolute path passes through untouched."""
    if not name:
        return ""
    if Path(name).is_absolute():
        return name
    stem = name.lower().replace(" ", "-")
    for d in FONT_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if f.suffix.lower() in (".ttf", ".otf") and f.stem.lower().replace(" ", "-") == stem:
                return str(f)
    raise SystemExit(f"font {name!r} not installed under {[str(d) for d in FONT_DIRS]}; "
                     "install the TTF, or give the absolute path to the file in the scene JSON")


def resolve(spec: Dict[str, Any], base: Optional[Path], ratio: Optional[str] = None,
            scale: float = 1.0, still: bool = False, seconds: Optional[float] = None) -> Dict[str, Any]:
    spec = json.loads(json.dumps(spec))  # deep copy
    out = spec.setdefault("output", {})
    if still:
        out["kind"] = "still"
    out.setdefault("kind", "still")
    if seconds is not None:
        out["seconds"] = seconds
    r = ratio or out.get("ratio", "9:16")
    if ratio or "w" not in out or "h" not in out:
        w, h = ratio_dims(r)
        out["w"], out["h"] = w, h
    out["ratio"] = r
    if scale != 1.0:
        out["w"] = max(16, int(out["w"] * scale) // 2 * 2)
        out["h"] = max(16, int(out["h"] * scale) // 2 * 2)
    for o in spec.get("objects", []):
        if o.get("font"):
            o["font"] = font_path(o["font"])
        if o.get("file") and base is not None and not Path(o["file"]).is_absolute():
            o["file"] = str((base / o["file"]).resolve())
        if o.get("file") and not Path(o["file"]).exists():
            raise SystemExit(f"missing file for object {o.get('name') or o.get('type')}: {o['file']}")
    return spec


def _mux(frames: Path, fps: int, out_mp4: Path) -> Path:
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH. Install it (brew install ffmpeg / apt install ffmpeg / "
                         "winget install ffmpeg), or keep the PNG frames and mux them yourself.")
    cmd = ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(frames / "f_%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(out_mp4)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out_mp4.exists():
        raise RuntimeError(f"ffmpeg mux failed: {proc.stderr[-400:]}")
    return out_mp4


def render_scene(spec: Dict[str, Any], out_dir: Path, base: Optional[Path] = None, **kw) -> Path:
    spec = resolve(spec, base, **kw)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    resolved = out_dir / "scene.resolved.json"
    resolved.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    t0 = time.time()
    cmd = [blender_bin(), "-b", "--python", str(BPY), "--", str(resolved), str(out_dir)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    log = out_dir / "blender.log"
    log.write_text((proc.stdout or "") + "\n" + (proc.stderr or ""), encoding="utf-8")
    if proc.returncode != 0 or "SCENE DONE" not in (proc.stdout or ""):
        tail = ((proc.stderr or "") + (proc.stdout or ""))[-600:]
        raise RuntimeError(f"blender render failed (rc={proc.returncode}); see {log}\n{tail}")
    out = spec["output"]
    if out["kind"] == "sequence":
        frames = out_dir / "frames"
        n = len(sorted(frames.glob("f_*.png")))
        result = _mux(frames, int(out.get("fps", 24)), out_dir / "render.mp4")
    else:
        n = 1
        result = out_dir / "still.png"
        if not result.exists():
            raise RuntimeError(f"still not written; see {log}")
    version = next((ln for ln in (proc.stdout or "").splitlines() if ln.startswith("Blender ")), "")
    (out_dir / "render.json").write_text(json.dumps({
        "result": str(result), "kind": out["kind"], "dims": [out["w"], out["h"]], "frames": n,
        "fps": out.get("fps", 24), "seconds": out.get("seconds") if out["kind"] == "sequence" else None,
        "blender": version.strip(), "spec_sha256": hashlib.sha256(resolved.read_bytes()).hexdigest(),
        "wall_seconds": round(time.time() - t0, 1),
    }, indent=2), encoding="utf-8")
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("scene", nargs="?", help="scene JSON path")
    ap.add_argument("--out", help="output directory (default: <scene dir>/render/<scene stem>)")
    ap.add_argument("--still", action="store_true", help="render one frame as still.png")
    ap.add_argument("--ratio", help="9:16 | 16:9 | 4:5 | 1:1 (overrides the spec)")
    ap.add_argument("--scale", type=float, default=1.0, help="proof scale, e.g. 0.35")
    ap.add_argument("--seconds", type=float, help="override sequence length")
    ap.add_argument("--list-ratios", action="store_true")
    a = ap.parse_args(argv)
    if a.list_ratios:
        for k, (w, h) in RATIOS.items():
            print(f"{k}\t{w}x{h}")
        return 0
    if not a.scene:
        ap.error("give a scene JSON")
    path = Path(a.scene)
    if not path.exists():
        raise SystemExit(f"no such scene: {path}")
    spec = json.loads(path.read_text(encoding="utf-8"))
    out_dir = Path(a.out) if a.out else path.parent / "render" / path.stem
    result = render_scene(spec, out_dir, base=path.parent, ratio=a.ratio, scale=a.scale,
                          still=a.still, seconds=a.seconds)
    meta = json.loads((out_dir / "render.json").read_text())
    print(f"{result}  {meta['dims'][0]}x{meta['dims'][1]}  frames={meta['frames']}  {meta['wall_seconds']}s  {meta['blender']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
