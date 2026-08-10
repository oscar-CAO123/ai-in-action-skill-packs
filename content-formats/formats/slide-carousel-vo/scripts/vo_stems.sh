#!/usr/bin/env bash
# cio-1981 VO. One ElevenLabs stem per line so line boundaries are exact (the still cuts are
# timed off them), then joined with the click-free chain from engine/tools/vo_utils.py.
# NEVER loudnorm: it pumps between lines and reintroduces the clicks this chain exists to kill.
# Usage: ./bin_vo.sh [voice_id]
set -euo pipefail
cd "$(dirname "$0")"
ENGINE="../../engine"
VOICE="${1:-UmQN7jS1Ee8B1czsUtQh}"   # Theo Silk, the engine config's canonical house voice (pipeline.config.json)
KEY=$(grep -m1 '^ELEVENLABS_API_KEY=' "$ENGINE/config/.env" | cut -d= -f2- | tr -d '"'"'"' \r')
[ -n "$KEY" ] || { echo "no ELEVENLABS_API_KEY"; exit 1; }
mkdir -p vo/stems

i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  i=$((i+1))
  N=$(printf '%02d' "$i")
  OUT="vo/stems/${N}.mp3"
  if [ -f "$OUT" ]; then echo "[skip] $OUT"; continue; fi
  python3 -c "
import json,sys,urllib.request
body=json.dumps({'text':sys.argv[1],'model_id':'eleven_multilingual_v2',
 'voice_settings':{'stability':0.4,'similarity_boost':0.75,'style':0.0,'use_speaker_boost':True}}).encode()
req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+sys.argv[2],data=body,
 headers={'xi-api-key':sys.argv[3],'Content-Type':'application/json'})
open(sys.argv[4],'wb').write(urllib.request.urlopen(req).read())
" "$line" "$VOICE" "$KEY" "$OUT"
  echo "[vo] $OUT  $(printf '%.60s' "$line")"
done < vo/lines.txt
echo "[vo] $i stems in vo/stems/"
