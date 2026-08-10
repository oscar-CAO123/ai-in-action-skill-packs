#!/usr/bin/env bash
# Finish the carousel cut: VHS grade the body, mix the clunks under the VO, append the clean end
# card, burn captions.
#
# Order matters. The VHS grade goes on the BODY only, before captions, so the tape damage lands on
# the painted slides and the type stays crisp. The end card is never graded: it is the brand card.
# Chain is the camcorder grade from the old build (bin_vhs_video.sh), unchanged.
set -euo pipefail
cd "$(dirname "$0")"
ENDCARD="../../engine/config/brand/endcard-client-9x16.png"
CLUNK="${1:-sfx/clunk-a.mp3}"
TICK="${2:-sfx/tick-softer.mp3}"

# 1. VHS grade. noise allf=t+u animates per frame, which is what makes the grain crawl.
ffmpeg -nostdin -y -v error -i work/carousel_body.mp4 -vf "\
scale=486:-2:flags=bilinear,scale=1080:1920:flags=bilinear,\
gblur=sigma=0.7,\
rgbashift=rh=6:bh=-5:gh=1,\
eq=contrast=0.94:brightness=0.05:saturation=1.08:gamma=1.06,\
colorbalance=rs=0.07:gs=0.01:bs=-0.07:rm=0.04:bm=-0.04,\
noise=alls=16:allf=t+u,\
drawgrid=w=0:h=3:t=1:c=black@0.05,\
curves=all='0/0.10 0.5/0.52 1/0.93',\
vignette=PI/5" \
-c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -an work/carousel_vhs.mp4

# 2. Audio: VO plus one clunk per major change, each delayed to its cue and mixed under the read.
/usr/bin/python3 - "$CLUNK" "$TICK" <<'PY'
import json, subprocess, sys
clunk, tick = sys.argv[1], sys.argv[2]
cues = json.load(open("sfx/cues.json"))
minor = json.load(open("sfx/cues_minor.json"))
ins, filt, tags = ["-i", "vo/vo.wav"], [], []
n = 0
for t in cues:                       # slide changes: the carousel clunk
    n += 1; ins += ["-i", clunk]
    filt.append(f"[{n}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.34[c{n}]")
    tags.append(f"[c{n}]")
for t in minor:                      # hard cuts: the quiet tick, well under the read
    n += 1; ins += ["-i", tick]
    filt.append(f"[{n}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.9[c{n}]")
    tags.append(f"[c{n}]")
filt.append("[0:a]" + "".join(tags) + f"amix=inputs={n+1}:normalize=0:duration=first[m]")
subprocess.run(["ffmpeg","-nostdin","-y","-v","error"] + ins +
    ["-filter_complex", ";".join(filt), "-map", "[m]", "-ac","1","-ar","48000",
     "work/carousel_mix.wav"], check=True)
print(f"[mix] {len(cues)} clunks and {len(minor)} ticks under the VO")
PY

# 3. Mux, append the clean end card
ffmpeg -nostdin -y -v error -i work/carousel_vhs.mp4 -i work/carousel_mix.wav \
  -c:v copy -c:a aac -b:a 192k -shortest work/carousel_vo.mp4
ffmpeg -nostdin -y -v error -loop 1 -i "$ENDCARD" -t 3 -f lavfi -i anullsrc=r=48000:cl=mono \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest work/99-endcard.mp4
printf "file 'carousel_vo.mp4'\nfile '99-endcard.mp4'\n" > work/cfinal.txt
ffmpeg -nostdin -y -v error -f concat -safe 0 -i work/cfinal.txt -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 192k work/carousel_full.mp4

# 4. Captions last, so the type never goes through the tape grade
/usr/bin/python3 bin_captions.py work/carousel_full.mp4 work/words.json cio-1981-noir-carousel-9x16.mp4 --offset 0 --endclean 3.0
echo "[done] cio-1981-noir-carousel-9x16.mp4  $(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 cio-1981-noir-carousel-9x16.mp4)s"
