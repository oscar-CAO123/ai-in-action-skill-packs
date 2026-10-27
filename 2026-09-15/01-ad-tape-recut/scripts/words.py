"""Per-word timings for every film: transcripts/<stem>.words.json as [[start, end, word], ...].
Get all of them before the first render. Usage: words.py [stem ...]"""
import json, sys
from pathlib import Path
import whisper

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
SRC = Path(TAPE["source_dir"]).expanduser()          # ENV
OUT = HERE / "transcripts"
model = whisper.load_model(TAPE.get("whisper_model", "medium.en"))
stems = sys.argv[1:] or [p.stem for p in OUT.glob("*.json") if not p.stem.endswith(".words") and not (OUT / f"{p.stem}.words.json").exists()]
for stem in stems:
    v = [p for p in SRC.glob(TAPE["glob"]) if p.stem.replace(" ", "") == stem][0]
    r = model.transcribe(str(v), language="en", fp16=False, word_timestamps=True, condition_on_previous_text=False)
    w = [[round(x["start"], 2), round(x["end"], 2), x["word"].strip()] for s in r["segments"] for x in s.get("words", [])]
    json.dump(w, open(OUT / f"{stem}.words.json", "w")); print(stem, len(w), "words")
