"""Render recipes as media with sentence-safe cut points and faded joins.
Usage: cut.py T4 [T1 ...] | --all | --timelines
Writes cuts/<id>.mp4, cuts/<id>.cutlist.txt and cuts/<id>.timeline.json. Read references/cut-points.md."""
import json, subprocess, sys
from pathlib import Path

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV
BANK = {k: v for k, v in json.load(open(HERE / "bank.json")).items() if not k.startswith("_")}
RECIPES = {k: v for k, v in json.load(open(HERE / "recipes.json")).items() if not k.startswith("_")}
OUT = HERE / "cuts"; OUT.mkdir(exist_ok=True)
AN = {p.stem: json.load(open(p)) for p in (HERE / "analysis").glob("*.json") if not p.stem.startswith("_")}
WORDS = {p.stem.replace(".words", ""): json.load(open(p)) for p in (HERE / "transcripts").glob("*.words.json")}
TERM = (".", "?", "!")
OUT_W, OUT_H, FPS = TAPE.get("output", [720, 1280, 30])

def stem(prefix): return TAPE["films"][prefix]["stem"]
def src(prefix):
    m = [p for p in SRC.glob(TAPE["glob"]) if p.stem.replace(" ", "") == stem(prefix)]; assert len(m) == 1, stem(prefix); return m[0]
def parse(tok):
    if "@" in tok:
        sid, rng = tok.split("@"); a, b = map(float, rng.split("-")); return sid, a, b
    return tok, None, None

def snap(prefix, s, e):
    W = WORDS[stem(prefix)]; A = AN[stem(prefix)]; caps = A["caption_changes"]; sil = A["silence"]; notes = []
    cands = [i for i, (a, b, t) in enumerate(W) if s - 0.30 <= a <= s + 0.50]
    i0 = min(cands, key=lambda i: abs(W[i][0] - s)) if cands else next(i for i, (a, b, t) in enumerate(W) if a >= s)
    prev_end = W[i0 - 1][1] if i0 > 0 else 0.0
    w0 = W[i0][0]
    c = [x for x in caps if prev_end - 0.05 <= x <= w0 + 0.10]
    if c: s2 = max(c[-1], prev_end); notes.append(f"start on caption swap {c[-1]:.2f}")
    else: s2 = max(prev_end + 0.02, w0 - min(0.15, (w0 - prev_end) / 2)); notes.append("start by word gap")
    il = max(i for i, (a, b, t) in enumerate(W) if a < e - 0.10)
    if not W[il][2].endswith(TERM) and il < len(W) - 1:
        j = il
        while j + 1 < len(W) and W[j + 1][0] < e + 0.8 and not W[j][2].endswith(TERM): j += 1
        if W[j][2].endswith(TERM): notes.append(f"sentence finished +{W[j][1]-W[il][1]:.2f}s through '{W[j][2]}'"); il = j
        else:
            k = il
            while k > 0 and not W[k][2].endswith(TERM) and e - W[k][1] <= 2.5: k -= 1
            if W[k][2].endswith(TERM) and k < il: notes.append(f"trimmed back {W[il][1]-W[k][1]:.2f}s to '{W[k][2]}'"); il = k
            else: notes.append("WARNING ends mid-sentence (no terminal punctuation within 0.8s ahead or 2.5s back)")
    wl_end = W[il][1]; next_start = W[il + 1][0] if il + 1 < len(W) else wl_end + 1.0
    c = [x for x in caps if wl_end - 0.05 <= x <= next_start + 0.05]
    if c: e2 = max(wl_end, c[0] - 0.02); notes.append(f"end before caption swap {c[0]:.2f}")
    else: e2 = wl_end + min(0.30, max(0.06, (next_start - wl_end) * 0.6)); notes.append("end by word gap")
    e2 = min(e2, next_start - 0.02) if next_start > wl_end else e2
    if any(a <= e2 <= b for a, b in sil): notes.append("end inside a silence gap")
    return s2, e2, W[i0][2], W[il][2], notes

def write_timeline(rid, parts, duration):
    out = []; words = []; cur = 0.0
    for p, s2, e2, sid in parts:
        W = WORDS[stem(p)]; d = e2 - s2
        words += [[round(a - s2 + cur, 2), round(b - s2 + cur, 2), t] for a, b, t in W if a >= s2 - 0.05 and a < e2]
        out.append({"sid": sid, "film": p, "src": [round(s2, 2), round(e2, 2)], "cut": [round(cur, 2), round(cur + d, 2)]}); cur += d
    json.dump({"parts": out, "words": words, "duration": round(duration, 2)}, open(OUT / f"{rid}.timeline.json", "w"))

def render(rid):
    rec = RECIPES[rid]; raw = []
    for t in rec["segments"]:
        sid, a, b = parse(t); p, ss, ee, _, _ = BANK[sid]; s = ss if a is None else a; e = ee if b is None else b
        if raw and raw[-1][0] == p and s <= raw[-1][2] + 0.35 and s >= raw[-1][1]:
            raw[-1] = (p, raw[-1][1], e, raw[-1][3] + "+" + sid)
        else: raw.append((p, s, e, sid))
    plan = []
    for p, s, e, sid in raw:
        s2, e2, fw, lw, notes = snap(p, s, e); plan.append((p, s2, e2, sid, fw, lw, notes))
    args = ["ffmpeg", "-v", "error", "-y"]; fc = []
    for i, (p, s2, e2, *_) in enumerate(plan):
        args += ["-ss", f"{s2:.3f}", "-to", f"{e2:.3f}", "-i", str(src(p))]
        d = e2 - s2
        fc.append(f"[{i}:v]scale={OUT_W}:{OUT_H},fps={FPS},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        fc.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st={max(0, d-0.03):.3f}:d=0.03[a{i}]")
    n = len(plan); fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    out = OUT / f"{rid}.mp4"
    args += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    subprocess.run(args, check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip())
    lines = [f"{rid} · {d:.1f}s"] + [f"{sid} {p} {s2:.2f}-{e2:.2f} · '{fw}' ... '{lw}' · {'; '.join(notes)}" for p, s2, e2, sid, fw, lw, notes in plan]
    (OUT / f"{rid}.cutlist.txt").write_text("\n".join(lines) + "\n"); print("\n".join(lines)); print()
    write_timeline(rid, [(p, s2, e2, sid) for p, s2, e2, sid, *_ in plan], d)

def timelines_from_cutlists():
    for cl in sorted(OUT.glob("*.cutlist.txt")):
        rid = cl.stem.replace(".cutlist", ""); lines = cl.read_text().strip().split("\n"); d = float(lines[0].split("· ")[1].rstrip("s")); parts = []
        for ln in lines[1:]:
            sid, p, rng = ln.split(" ")[:3]; a, b = map(float, rng.split("-")); parts.append((p, a, b, sid))
        write_timeline(rid, parts, d); print("timeline", rid)

ids = sys.argv[1:]
if ids == ["--timelines"]: timelines_from_cutlists(); sys.exit()
if ids == ["--all"]: ids = list(RECIPES)
for rid in ids: render(rid)
