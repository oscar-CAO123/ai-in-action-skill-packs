#!/usr/bin/env python3
"""Run one Blender scene script in the background, at low priority, on a few CPU threads, and stop
it if the machine gets hot or the memory climbs.

    python3 monitor_render.py <scene_script.py> <output-directory> [proof|animation] [--threads 3]

The scene script is any bpy script that takes `-- <out_dir> <mode>` after Blender's own arguments,
the way motion_study_example.py does. `proof` renders a handful of frames at half size so you can
look before you spend the minutes; `animation` renders the full sequence.

Guards, sampled every five seconds while Blender runs:
  - resident memory above 4 GiB           -> stop
  - process CPU above 350% for two samples -> stop  (300% means three fully busy cores)
  - the OS reports thermal throttling      -> stop  (macOS only; other systems skip this check)
  - 15 minutes of wall clock               -> stop

These are guardrails, not a temperature or GPU measurement. They cannot promise the machine never
exceeds a hardware threshold. Nothing here uses the GPU: Blender is started with a fixed thread
count and the scene script chooses CPU rendering.

Writes <mode>.log, <mode>-usage.json (every sample) and <mode>-summary.json beside the output.
"""
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) < 2:
    sys.exit(__doc__)
script = Path(args[0]).resolve()
out = Path(args[1]).resolve()
mode = args[2] if len(args) > 2 else "proof"
threads = 3
if "--threads" in sys.argv:
    threads = int(sys.argv[sys.argv.index("--threads") + 1])
out.mkdir(parents=True, exist_ok=True)

SYSTEM = platform.system()


def blender_bin():
    env = os.environ.get("BLENDER")
    if env and (shutil.which(env) or Path(env).exists()):
        return env
    home = Path.home()
    candidates = {
        "Darwin": ["/Applications/Blender.app/Contents/MacOS/Blender", "/opt/homebrew/bin/blender"],
        "Linux": ["/usr/bin/blender", "/snap/bin/blender", "/usr/local/bin/blender", str(home / "blender" / "blender")],
        "Windows": [str(Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Blender Foundation" / d / "blender.exe")
                    for d in ("Blender 5.2", "Blender 5.1", "Blender 5.0", "Blender 4.5")],
    }.get(SYSTEM, [])
    for c in candidates:
        if Path(c).exists():
            return c
    found = shutil.which("blender")
    if found:
        return found
    sys.exit("Blender not found. Install Blender 5.2 LTS, put it on PATH, or set BLENDER=/path/to/blender.")


command = [blender_bin(), "-b", "-t", str(threads), "--python-exit-code", "1", "--python", str(script), "--", str(out), mode]
if SYSTEM != "Windows" and shutil.which("nice"):
    command = ["nice", "-n", "15"] + command


def usage(pid):
    """(cpu_percent, rss_mb) for a process, or (None, None) if it cannot be read."""
    if SYSTEM == "Windows":
        try:
            import psutil  # optional; pip install psutil for CPU/RSS sampling on Windows
            p = psutil.Process(pid)
            return p.cpu_percent(interval=None), round(p.memory_info().rss / 1048576, 1)
        except Exception:
            return None, None
    r = subprocess.run(["ps", "-p", str(pid), "-o", "%cpu=,rss="], capture_output=True, text=True)
    if r.returncode:
        return None, None
    raw = r.stdout.split()
    return (float(raw[0]) if raw else 0.0), (round(int(raw[1]) / 1024, 1) if len(raw) > 1 else 0.0)


def thermal():
    """(ok, text). Only macOS exposes a plain thermal status; elsewhere this is a no-op that passes."""
    if SYSTEM != "Darwin":
        return True, "n/a"
    r = subprocess.run(["pmset", "-g", "therm"], capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip()


start = time.monotonic()
samples = []
reason = None
with (out / f"{mode}.log").open("w") as log:
    popen_kw = {"stdout": log, "stderr": subprocess.STDOUT}
    if SYSTEM != "Windows":
        popen_kw["start_new_session"] = True
    proc = subprocess.Popen(command, **popen_kw)

    def stop_render():
        if proc.poll() is None:
            if SYSTEM == "Windows":
                proc.terminate()
            else:
                os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                if SYSTEM == "Windows":
                    proc.kill()
                else:
                    os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()

    import atexit
    atexit.register(stop_render)

    def interrupted(signum, frame):
        stop_render()
        sys.exit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)

    while proc.poll() is None:
        cpu, rss = usage(proc.pid)
        t_ok, t_text = thermal()
        sample = {"elapsed": round(time.monotonic() - start, 1), "cpu_percent": cpu, "rss_mb": rss,
                  "thermal": t_text, "thermal_check_ok": t_ok}
        samples.append(sample)
        (out / f"{mode}-usage.json").write_text(json.dumps(samples, indent=2))
        limits = re.findall(r"(?:CPU_Speed_Limit|Scheduler_Limit)\s*=\s*(\d+)", t_text)
        if rss is not None and rss > 4096:
            reason = "Blender RSS exceeded 4 GiB"
        if any(int(v) < 100 for v in limits):
            reason = "the OS reported CPU throttling"
        if re.search(r"(?:Thermal|Performance)_Warning_Level\s*=\s*[1-9]", t_text):
            reason = "the OS reported a thermal warning"
        if not t_ok:
            reason = "thermal status check failed"
        if len(samples) > 2 and all((x["cpu_percent"] or 0) > 350 for x in samples[-2:]):
            reason = "CPU exceeded 3.5 core equivalents for two samples"
        if time.monotonic() - start > 900:
            reason = "15 minute render budget reached"
        if reason:
            stop_render()
            break
        time.sleep(5)

    summary = {
        "mode": mode, "script": str(script), "exit_code": proc.returncode, "stop_reason": reason,
        "wall_seconds": round(time.monotonic() - start, 1),
        "peak_cpu_percent": max((x["cpu_percent"] or 0 for x in samples), default=0),
        "peak_rss_mb": max((x["rss_mb"] or 0 for x in samples), default=0),
        "samples": len(samples), "device": "CPU", "threads": threads,
        "note": "CPU percent is per core: 300% equals three cores. Sampled RSS and OS warnings are guardrails, "
                "not a temperature or GPU measurement.",
    }
    (out / f"{mode}-summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))
sys.exit(1 if reason else (proc.returncode or 0))
