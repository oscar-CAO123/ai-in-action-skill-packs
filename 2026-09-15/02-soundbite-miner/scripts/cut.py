"""Download every kept clip's section from YouTube (one yt-dlp call per video, all its sections),
then file each as clips/<speaker>/n###_<id>_<slug>.mp4. Read-only on YouTube, rerunnable, skips
what exists, ordered by rank so the best clips land first. Usage: cut.py [offset stride] to shard."""
import json, subprocess, re, time, sys, shutil
from pathlib import Path

H = Path.cwd()
clips = json.load(open(H / "clips.json"))
PAD0, PAD1 = 0.8, 1.0
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]
def dest(c): return H / "clips" / c["speaker"] / f"n{c['n']:03d}_{c['id']}_{slug(c['hook'])}.mp4"
byvid = {}
for c in clips:
    if dest(c).exists(): continue
    byvid.setdefault(c["id"], []).append(c)
order = sorted(byvid, key=lambda v: min(c["n"] for c in byvid[v]))
if len(sys.argv) > 2: order = order[int(sys.argv[1])::int(sys.argv[2])]
print("videos to fetch", len(order), "clips", sum(len(byvid[v]) for v in order), flush=True)
for vid in order:
    cs = byvid[vid]; raw = H / "raw" / vid; raw.mkdir(parents=True, exist_ok=True)
    secs = []
    for c in cs: secs += ["--download-sections", f"*{max(0, c['t0']-PAD0):.2f}-{c['t1']+PAD1:.2f}"]
    ok = False
    for client in ("android", "web_embedded", "mweb", "ios"):
        args = ["yt-dlp", "-q", "--no-warnings", "--extractor-args", f"youtube:player_client={client}",
                "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]/b", "--merge-output-format", "mp4",
                "--force-keyframes-at-cuts", *secs, "-o", str(raw / "%(section_start)s.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"]
        r = subprocess.run(args, capture_output=True, text=True)
        if list(raw.glob("*.mp4")): ok = True; break
        (H / "raw" / "errors.log").open("a").write(f"{vid} {client}: {r.stderr.strip()[-300:]}\n"); time.sleep(4)
    if not ok: print("FAIL", vid, flush=True); continue
    for c in cs:
        want = f"{max(0, c['t0']-PAD0):.2f}"
        cand = [p for p in raw.glob("*.mp4") if abs(float(p.stem) - float(want)) < 0.6]
        if not cand: print("  missing section", vid, want, flush=True); continue
        d = dest(c); d.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(cand[0]), d)
    print("ok", vid, len(cs), flush=True); time.sleep(3)
print("DONE")
