#!/usr/bin/env bash
# Voiceover stems. One ElevenLabs text-to-speech stem per line of vo/lines.txt, so line boundaries are
# exact (the still cuts are timed off them). join_vo.py then joins them with the click-free chain.
# NEVER loudnorm: it pumps between lines and reintroduces the clicks this chain exists to kill.
# Usage: ./vo_stems.sh <voice_id>     (a voice id from your own ElevenLabs voice library)
# The key comes from VOICE_API_KEY in engine/config/.env and travels in the environment, so it is
# never on the command line.
set -euo pipefail
cd "$(dirname "$0")"
ENGINE="../../engine"
VOICE="${1:?pass a voice id from your voice library}"
VOICE_API_KEY=$(grep -m1 '^VOICE_API_KEY=' "$ENGINE/config/.env" 2>/dev/null | cut -d= -f2- | tr -d '"'"'"' \r' || true)
[ -n "$VOICE_API_KEY" ] || { echo "no VOICE_API_KEY in $ENGINE/config/.env"; exit 1; }
export VOICE_API_KEY
mkdir -p vo/stems

i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  i=$((i+1))
  N=$(printf '%02d' "$i")
  OUT="vo/stems/${N}.mp3"
  if [ -f "$OUT" ]; then echo "[skip] $OUT"; continue; fi
  python3 -c "
import json,os,sys,urllib.request
body=json.dumps({'text':sys.argv[1],'model_id':'eleven_multilingual_v2',
 'voice_settings':{'stability':0.4,'similarity_boost':0.75,'style':0.0,'use_speaker_boost':True}}).encode()
req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+sys.argv[2],data=body,
 headers={'xi-api-key':os.environ['VOICE_API_KEY'],'Content-Type':'application/json'})
audio=urllib.request.urlopen(req).read()
open(sys.argv[3],'wb').write(audio)
" "$line" "$VOICE" "$OUT"
  echo "[vo] $OUT  $(printf '%.60s' "$line")"
done < vo/lines.txt
echo "[vo] $i stems in vo/stems/"
