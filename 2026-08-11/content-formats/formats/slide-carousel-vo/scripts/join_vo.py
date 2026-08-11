#!/usr/bin/env python3
"""Join the cio-1981 VO stems click-free and emit exact per-line start times.

Trim each stem's own head/tail silence FIRST, then butt them together over controlled gaps.
Doing it in that order means the line offsets stay exact, which the still cuts are timed off.
Fade-to-zero at every join (10ms) so no join lands on a non-zero sample. Static peak
normalisation only, never loudnorm, which pumps between lines and reintroduces clicks.
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
STEMS = sorted((HERE / "vo/stems").glob("*.mp3"))
LINES = [l for l in (HERE / "vo/lines.txt").read_text.splitlines if l.strip]
assert len(STEMS) == len(LINES), f"{len(STEMS)} stems vs {len(LINES)} lines"

# Beat after each line. Longer at the turns: after 2 (hook into the setup), after 9 (the title is
# named), after 12 (resolution into the lesson), after 15 (into the present), and either side of
# 18, because "Doubt it." only lands dry with air around it.
GAP = {2: 0.25, 5: 0.20, 8: 0.25, 11: 0.25, 14: 0.30, 16: 0.20, 17: 0.35, 18: 0.20}
DEFAULT_GAP = 0.12
WORK = HERE / "work"; WORK.mkdir(exist_ok=True)
TRIM = WORK / "stems_trim"; TRIM.mkdir(exist_ok=True)


def run(a):
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode:
        sys.exit(p.stderr[-800:])
    return p


def dur(f):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(f)],
        capture_output=True, text=True).stdout.strip)


def edges(f):
    """First and last non-silent moment, so we trim the model's own head/tail padding."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f),
                        "-af", "silencedetect=noise=-40dB:d=0.06", "-f", "null", "-"],
                       capture_output=True, text=True)
    total = dur(f)
    starts = [float(x) for x in re.findall(r"silence_start:\s*([-\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", p.stderr)]
    head = ends[0] if ends and starts and starts[0] <= 0.05 else 0.0
    # The last silence is only the TAIL if it actually runs to the end of the file. On a stem whose
    # trailing silence has already been tightened away, the last silence is an internal pause, and
    # treating it as the tail cuts real speech off the end of the line.
    tail = total
    if starts:
        runs_to_eof = len(starts) > len(ends) or (ends and ends[-1] >= total - 0.06)
        if runs_to_eof and starts[-1] > head and (total - starts[-1]) > 0.12:
            tail = starts[-1]
    return max(0.0, head - 0.03), min(total, tail + 0.10)


timeline, t = [], 0.0
concat = WORK / "vo_concat.txt"
parts = []
for i, (stem, line) in enumerate(zip(STEMS, LINES), start=1):
    a, b = edges(stem)
    out = TRIM / f"{i:02d}.wav"
    d = b - a
    run(["ffmpeg", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(stem),
         "-af", f"afade=t=in:st=0:d=0.010,afade=t=out:st={max(0,d-0.010):.3f}:d=0.010,aresample=48000",
         "-ac", "1", "-ar", "48000", str(out)])
    real = dur(out)
    timeline.append({"n": i, "line": line, "start": round(t, 3), "end": round(t + real, 3)})
    parts.append(out)
    gap = GAP.get(i, DEFAULT_GAP) if i < len(STEMS) else 0.0
    t += real + gap

# Build with explicit silence padding between parts so the gaps are exact.
inputs, filters = [], []
for i, p in enumerate(parts):
    inputs += ["-i", str(p)]
    filters.append(f"[{i}:a]")
    gap = GAP.get(i + 1, DEFAULT_GAP) if i < len(parts) - 1 else 0.0
    if gap:
        filters.append(f"aevalsrc=0:d={gap}:s=48000:c=mono[g{i}];")
fc = ""
seq = []
gi = 0
for i, p in enumerate(parts):
    seq.append(f"[{i}:a]")
    gap = GAP.get(i + 1, DEFAULT_GAP) if i < len(parts) - 1 else 0.0
    if gap:
        fc += f"aevalsrc=0:d={gap}:s=48000:c=mono[g{gi}];"
        seq.append(f"[g{gi}]")
        gi += 1
fc += "".join(seq) + f"concat=n={len(seq)}:v=0:a=1[j]"
run(["ffmpeg", "-y"] + inputs + ["-filter_complex", fc, "-map", "[j]",
     "-ac", "1", "-ar", "48000", str(WORK / "vo_raw.wav")])

# Static peak normalisation to -1.5 dBFS. Static on purpose.
p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(WORK / "vo_raw.wav"),
                    "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
mv = float(re.search(r"max_volume:\s*(-?[\d.]+) dB", p.stderr).group(1))
run(["ffmpeg", "-y", "-i", str(WORK / "vo_raw.wav"), "-af", f"volume={-1.5 - mv:.2f}dB",
     "-ac", "1", "-ar", "48000", str(HERE / "vo/vo.wav")])
run(["ffmpeg", "-y", "-i", str(HERE / "vo/vo.wav"), "-b:a", "192k", str(HERE / "vo/vo.mp3")])

total = dur(HERE / "vo/vo.wav")
(HERE / "vo/timeline.json").write_text(json.dumps({"total": round(total, 3), "lines": timeline}, indent=2))
print(f"vo/vo.wav  {total:.2f}s  peak-normalised {-1.5 - mv:+.2f} dB")
for e in timeline:
    print(f"  L{e['n']:02d}  {e['start']:6.2f} -> {e['end']:6.2f}  {e['line'][:58]}")
