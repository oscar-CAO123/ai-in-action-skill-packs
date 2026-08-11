#!/usr/bin/env python3
"""Align whisper's word timings to the script, exactly.

Whisper is the timing source and the script is the spelling source. Three things it gets wrong,
each of which silently breaks the captions or the cut:

  1. it prefixes its own marker onto the first token ("inaccIn")
  2. it swallows a word occasionally ("And now… Who runs the world?" loses "look"), and every
     timing after the gap then belongs to the wrong word
  3. it writes what it heard, not what was written ("60s" for "sixties")

Output is one entry per SCRIPT token, in order, so downstream code can index straight into it by
line and offset. A word whisper missed gets a zero-width slot at the following word's onset, which
still renders as a caption because each word shows until the next word's onset.

Usage: align_words.py <words_raw.json> <lines.txt> <words.json>
"""
import json
import re
import sys


def norm(x):
    return re.sub(r"[^a-z0-9]", "", x.lower)


def main:
    raw_path, lines_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    raw = json.load(open(raw_path))
    if raw:
        raw[0][2] = re.sub(r"^inacc", "", raw[0][2])
    toks = [w for l in open(lines_path).read.splitlines if l.strip for w in l.split]

    out, i, j, inserted = [], 0, 0, []
    while i < len(toks):
        if j < len(raw) and norm(toks[i]) == norm(raw[j][2]):
            out.append([raw[j][0], raw[j][1], toks[i]])
            i += 1
            j += 1
            continue
        prev_end = out[-1][1] if out else 0.0
        nxt = raw[j][0] if j < len(raw) else prev_end
        s = min(prev_end, nxt)
        out.append([round(s, 3), round(max(s, nxt), 3), toks[i]])
        inserted.append(toks[i])
        i += 1

    json.dump(out, open(out_path, "w"))
    print(f"[align] {len(out)} words, {len(inserted)} inserted {inserted if inserted else ''}")
    if len(raw) > len(toks):
        print(f"[warn] whisper returned {len(raw)} tokens against {len(toks)} in the script; "
              f"check the tail of {out_path}")


if __name__ == "__main__":
    main
