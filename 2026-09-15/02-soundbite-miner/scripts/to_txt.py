"""json3 auto-captions to transcripts/<id>.txt: a header from meta and episodes.tsv, then the words
with a [mm:ss] stamp every ~15 s of speech. Run from the workspace."""
import json, glob
from pathlib import Path

H = Path.cwd(); (H / "transcripts").mkdir(exist_ok=True)
eps = {l.split("\t")[1]: l.rstrip("\n").split("\t") for l in open(H / "inv/episodes.tsv") if l.strip()}
def ts(ms): s = int(ms / 1000); return f"[{s//60:02d}:{s%60:02d}]"
n = 0
for vid, row in eps.items():
    fs = sorted(glob.glob(str(H / f"subs/{vid}.en-orig.json3"))) or sorted(glob.glob(str(H / f"subs/{vid}.*.json3")))
    if not fs: continue
    ev = json.load(open(fs[0])).get("events", [])
    words = []
    for e in ev:
        t0 = e.get("tStartMs", 0)
        for s in e.get("segs", []):
            w = s.get("utf8", "").replace("\n", " ").strip()
            if w: words.append((t0 + s.get("tOffsetMs", 0), w))
    m = (H / f"meta/{vid}.txt").read_text().strip().split("\t") if (H / f"meta/{vid}.txt").exists() else ["?", "?", "?", "?", "?"]
    who, _, dur, ch, title = row[:5]
    out = [f"# {title}", f"# speaker={who} id={vid} channel={ch} uploaded={m[0]} views={m[1]} duration={int(float(dur))//60}m", ""]
    line = []; last = -1e9
    for t, w in words:
        if t - last >= 15000:
            if line: out.append(" ".join(line))
            line = [ts(t)]; last = t
        line.append(w)
    if line: out.append(" ".join(line))
    (H / f"transcripts/{vid}.txt").write_text("\n".join(out)); n += 1
print(n, "transcripts")
