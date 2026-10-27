"""Verify every mined clip against the caption words and pin exact start and end times.
Reads mined/*.json, subs/<id>.*.json3, inv/episodes.tsv, meta/, speakers.json.
Writes clips.json (kept, ranked) and rejected.json (with reasons). Run from the workspace."""
import json, glob, re, collections
from pathlib import Path

H = Path.cwd()
SP = json.load(open(H / "speakers.json"))
HOST_CHANNELS = {c for v in SP.values() for c in v.get("host_channels", [])}
NAMES = [v["name"].lower() for v in SP.values()] + [p for v in SP.values() for p in v["name"].lower().split()]
eps = {l.split("\t")[1]: l.rstrip("\n").split("\t") for l in open(H / "inv/episodes.tsv") if l.strip()}
meta = {p.stem: p.read_text().strip().split("\t") for p in (H / "meta").glob("*.txt")}
def norm(s): return re.findall(r"[a-z0-9']+", s.lower().replace("’", "'"))
WORDS = {}
def words(vid):
    if vid in WORDS: return WORDS[vid]
    fs = glob.glob(str(H / f"subs/{vid}.en-orig.json3")) or glob.glob(str(H / f"subs/{vid}.*.json3"))
    out = []
    for e in json.load(open(fs[0])).get("events", []):
        t0 = e.get("tStartMs", 0)
        for s in e.get("segs", []):
            for w in norm(s.get("utf8", "")): out.append((t0 + s.get("tOffsetMs", 0), w))
    res = [(t / 1000, (out[i + 1][0] / 1000 if i + 1 < len(out) else t / 1000 + 0.6), w) for i, (t, w) in enumerate(out)]
    WORDS[vid] = res; return res
def mmss(s): m, s2 = s.split(":"); return int(m) * 60 + int(s2)
clips = []; rej = []
for f in sorted(glob.glob(str(H / "mined/*.json"))):
    for c in json.load(open(f)):
        vid = c["id"]
        if vid not in eps: rej.append({**c, "reason": "unknown id"}); continue
        W = words(vid); s0 = mmss(c["start"]) - 25; e0 = mmss(c["end"]) + 40
        win = [w for w in W if s0 <= w[0] <= e0]; wt = [w[2] for w in win]
        q = norm(c["quote"])
        if len(q) < 8: rej.append({**c, "reason": "quote too short"}); continue
        bag = set(wt); cov = sum(1 for t in q if t in bag) / len(q)
        def anchors(toks, latest):
            hits = []
            for i in range(len(toks) - 2):
                tri = toks[i:i + 3]
                for j in range(len(wt) - 2):
                    if wt[j:j + 3] == tri: hits.append(j); break
            if not hits: return None
            return max(hits) if latest else min(hits)
        hi = anchors(q[:14], False); ti = anchors(q[-14:], True)
        if cov < 0.45: rej.append({**c, "reason": f"no match cov={cov:.2f}"}); continue
        prec = "anchored" if (hi is not None and ti is not None) else ("loose" if (hi is None and ti is None) else "half")
        st = win[hi][0] if hi is not None else mmss(c["start"])
        en = win[min(ti + 2, len(win) - 1)][1] if ti is not None else mmss(c["end"]) + 15
        if en <= st or en - st < 8: rej.append({**c, "reason": f"bad span {st:.1f}-{en:.1f}"}); continue
        if en - st > 170: rej.append({**c, "reason": f"too long {en-st:.0f}s"}); continue
        c["precision"] = prec
        m = meta.get(vid, ["?", "?"])
        title = eps[vid][4]; channel = eps[vid][3]
        host_mode = channel in HOST_CHANNELS and not any(n in title.lower() for n in NAMES)
        clips.append({**c, "t0": round(st, 2), "t1": round(en, 2), "dur": round(en - st, 1), "cov": round(cov, 2),
                      "title": title, "channel": channel, "uploaded": m[0], "host_mode": host_mode})
clips.sort(key=lambda c: (c["id"], -c["score"], -c["dur"]))
kept = []
for c in clips:
    dup = False
    for k in kept:
        if k["id"] == c["id"]:
            ov = min(k["t1"], c["t1"]) - max(k["t0"], c["t0"])
            if ov > 0 and ov / min(k["dur"], c["dur"]) > 0.5: dup = True; break
    if not dup: kept.append(c)
for i, c in enumerate(sorted(kept, key=lambda c: (-c["score"], c["relevance"] != "core", c["speaker"], c["id"], c["t0"]))): c["n"] = i + 1
kept.sort(key=lambda c: c["n"])
json.dump(kept, open(H / "clips.json", "w"), indent=1); json.dump(rej, open(H / "rejected.json", "w"), indent=1)
print("kept", len(kept), "rejected", len(rej), collections.Counter(r["reason"].split()[0] for r in rej))
print(collections.Counter(c["speaker"] for c in kept), "host_mode", sum(c["host_mode"] for c in kept), "total min", round(sum(c["dur"] for c in kept) / 60))
hm = [c for c in kept if c["host_mode"]]
if hm:
    (H / "speaker_check.md").write_text("# Speaker check: host-mode episodes\n\nStrike any line that is the guest, then delete those ids from clips.json.\n\n" +
        "\n".join(f"- n{c['n']:03d} · {c['speaker']} · {c['title'][:60]} · {c['hook']}" for c in hm) + "\n")
    print(len(hm), "host-mode clips listed in speaker_check.md")
