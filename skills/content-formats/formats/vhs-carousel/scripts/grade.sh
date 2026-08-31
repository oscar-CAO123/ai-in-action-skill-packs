#!/usr/bin/env bash
# The tape grade for F12. Matched to the reference set, NOT to the talkshow grade.
#
# The house already owns a VHS grade at content-engine/ideas/talkshow-vsl/bin/vhs-grade.sh.
# That one emulates tube cameras dubbed to VHS: 8px rgbashift, hard scanlines, barrel
# distortion. The F12 reference carries none of those (chroma mis-registration measured 0px
# on all twelve slides, no scanline periodicity on nine of twelve). What it does carry is a
# heavy grain floor (6.97 to 12.17), a saturation cast that changes per plate (0.054 to
# 0.635) and a black floor that is usually crushed and occasionally milky.
#
# So: softness, grain, per-plate cast, black floor, mild bloom and vignette. Nothing else.
#
# Usage: ./grade.sh <in.png> <out.png> [sat] [black_lift] [soft_div] [grain]
#   sat        saturation multiplier, 0.05 near-monochrome .. 1.6 heavy cast   (default 1.15)
#   black_lift 0.00 crushed .. 0.12 milky dub blacks                           (default 0.02)
#   soft_div   resolution loss, 1.6 mild .. 3.0 heavy                          (default 2.2)
#   grain      noise strength, 30 light .. 70 heavy                            (default 48)
#
# On grain: this argument is ffmpeg's `noise=alls`, and it is NOT the number measure.py
# reports. Measured on a sweep, the grain floor lands at about alls/5.5 (alls 16 -> 3.2,
# 30 -> 5.6, 48 -> 8.7). The reference sits at 6.97 to 12.17, so the usable range is
# roughly alls 38 to 67, and anything near 16 renders far too clean to read as tape.
set -euo pipefail
IN="$1"; OUT="$2"
SAT="${3:-1.15}"; LIFT="${4:-0.02}"; SOFT="${5:-2.2}"; GRAIN="${6:-48}"

read W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN" | tr ',' ' ')
DW=$(python3 -c "print(max(2, int($W/$SOFT))//2*2)")

# format=gbrp before the split is load-bearing. Left in YUV, the screen blend below runs
# on the chroma planes as well as luma, which drives U and V toward full and turns every
# plate magenta. Bloom is an RGB operation.
ffmpeg -y -loglevel error -i "$IN" -filter_complex "\
[0:v]scale=${DW}:-2:flags=bilinear,scale=${W}:${H}:flags=bilinear,\
eq=contrast=1.06:saturation=${SAT}:brightness=0.01:gamma=1.02,\
gblur=sigma=0.7,format=gbrp,split=2[base][hl];\
[hl]curves=all='0/0 0.72/0 0.88/0.78 1/1',gblur=sigma=14[bloom];\
[base][bloom]blend=all_mode=screen:all_opacity=0.45,\
noise=alls=${GRAIN}:allf=t+u,\
vignette=PI/5,\
curves=all='0/${LIFT} 0.5/0.5 1/0.98'[out]" \
-map "[out]" -frames:v 1 "$OUT"
echo "[tape] $(basename "$IN") -> $(basename "$OUT")  sat=${SAT} lift=${LIFT} soft=${SOFT} grain=${GRAIN}"
