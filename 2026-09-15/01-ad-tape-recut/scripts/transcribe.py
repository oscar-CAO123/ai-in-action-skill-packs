"""Transcribe every source film with local Whisper. Read-only on the source.
Writes transcripts/<stem>.json (segments), transcripts/<stem>.txt and transcripts/ALL.md.
Run from the workspace that holds tape.json."""
import json, time
from pathlib import Path
import whisper

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV: where the export sits
OUT = HERE / "transcripts"; OUT.mkdir(exist_ok=True)
model = whisper.load_model(TAPE.get("whisper_model", "medium.en"))   # ENV: small.en on a low-RAM machine

vids = sorted(SRC.glob(TAPE["glob"]))
for i, v in enumerate(vids, 1):
    stem = v.stem.replace(" ", "")
    jp = OUT / f"{stem}.json"
    if jp.exists():
        print("skip", stem, flush=True); continue
    t0 = time.time()
    r = model.transcribe(str(v), language="en", fp16=False, word_timestamps=True, condition_on_previous_text=False)
    segs = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()} for s in r["segments"]]
    json.dump({"file": v.name, "text": r["text"].strip(), "segments": segs}, open(jp, "w"), indent=1)
    (OUT / f"{stem}.txt").write_text("\n".join(f"[{s['start']:06.2f}-{s['end']:06.2f}] {s['text']}" for s in segs) + "\n")
    print(f"{i}/{len(vids)} {stem} {len(r['text'].split())}w {time.time()-t0:.0f}s", flush=True)

parts = []
for p in sorted(OUT.glob("*.json")):
    if p.stem.endswith(".words"): continue
    d = json.load(open(p))
    parts.append(f"## {p.stem}\n\n" + "\n".join(f"[{s['start']:06.2f}] {s['text']}" for s in d["segments"]))
(OUT / "ALL.md").write_text("# Every transcript\n\n" + "\n\n".join(parts) + "\n")
print("ALL DONE")
