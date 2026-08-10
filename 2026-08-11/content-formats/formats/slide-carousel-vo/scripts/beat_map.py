#!/usr/bin/env python3
"""Build the beat map: one entry per POINT, cut to the voiceover's own word timings.

Reads beats.config.json in the project folder:

  {
    "splits": {"0": [2, 8], "1": [4]},        # line index -> token offsets where a new beat starts
    "stills": ["01-opener", "02-two-men"],    # one still slug per beat, in order
    "focal":  {"01-opener": [0.42, 0.56]}     # optional; anything missing defaults to centre-ish
  }

A beat can therefore start mid-sentence, on the exact word. The first beat of each spoken line is
flagged `major`, which is what the carousel treats as a slide change. Never try to detect majors by
comparing beat onsets to the stem starts in timeline.json: those are different measurements and the
match finds almost nothing.

Usage: beat_map.py [project_dir]
"""
import json
import os
import sys

DEFAULT_FOCAL = [0.45, 0.58]


def main():
    here = sys.argv[1] if len(sys.argv) > 1 else "."
    cfg = json.load(open(os.path.join(here, "beats.config.json")))
    raw = json.load(open(os.path.join(here, "work/words.json")))
    lines = [l.split() for l in open(os.path.join(here, "vo/lines.txt")).read().splitlines() if l.strip()]

    total_tokens = sum(len(t) for t in lines)
    if total_tokens != len(raw):
        sys.exit(f"words.json has {len(raw)} entries against {total_tokens} script tokens; "
                 f"run align_words.py first")

    def onset(i):
        while i < len(raw) - 1 and raw[i][1] <= raw[i][0]:
            i += 1
        return round(raw[i][0], 3)

    base, k = [], 0
    for t in lines:
        base.append(k)
        k += len(t)

    splits = {int(a): b for a, b in cfg["splits"].items()}
    stills = cfg["stills"]
    focal = cfg.get("focal", {})

    beats, majors, idx = [], [], 0
    for li, t in enumerate(lines):
        cuts = [0] + splits.get(li, []) + [len(t)]
        majors.append(idx)
        for a, b in zip(cuts, cuts[1:]):
            beats.append({"start": onset(base[li] + a), "text": " ".join(t[a:b])})
            idx += 1

    if len(beats) != len(stills):
        sys.exit(f"{len(beats)} beats against {len(stills)} stills in beats.config.json")
    if len(set(stills)) != len(stills):
        sys.exit("a still is listed twice; every beat gets its own image")

    for i, (bt, st) in enumerate(zip(beats, stills)):
        p = os.path.join(here, f"gen/{st}.png")
        if not os.path.exists(p):
            sys.exit(f"missing {p}")
        bt["still"] = st
        bt["fx"], bt["fy"] = focal.get(st, DEFAULT_FOCAL)
        bt["major"] = i in majors

    for i in range(1, len(beats)):
        if beats[i]["start"] < beats[i - 1]["start"]:
            sys.exit(f"beat {i} starts before beat {i-1}; the alignment is wrong")

    json.dump(beats, open(os.path.join(here, "work/beats.json"), "w"), indent=1)
    holds = [round(beats[i + 1]["start"] - b["start"], 2) for i, b in enumerate(beats[:-1])]
    print(f"[beats] {len(beats)} beats, {len(majors)} majors, "
          f"holds min {min(holds)} max {max(holds)} mean {round(sum(holds)/len(holds), 2)}")


if __name__ == "__main__":
    main()
