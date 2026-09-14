#!/usr/bin/env bash
# Read-only: auto-captions (json3) plus upload metadata for one video id. Skips if done.
# Usage: scripts/pull_subs.sh <id>     Loop it: for id in $(cut -f2 inv/episodes.tsv); do scripts/pull_subs.sh $id; sleep 3; done
id=$1; mkdir -p meta subs
[[ -f meta/$id.txt && -n "$(ls subs/$id.*json3 2>/dev/null)" ]] && exit 0
for c in android web_embedded mweb web; do
  yt-dlp -q --no-warnings --extractor-args "youtube:player_client=$c" --skip-download --write-auto-subs --write-subs \
    --sub-langs "en,en-orig,en-GB,en-US,en-AU" --sub-format json3 \
    --print-to-file "%(upload_date)s	%(view_count)s	%(uploader)s	%(duration)s	%(title)s" "meta/$id.txt" \
    -o "subs/%(id)s" "https://www.youtube.com/watch?v=$id" 2>>subs/err.log && [[ -f meta/$id.txt ]] && break
  sleep 2
done
ls subs/$id.*json3 >/dev/null 2>&1 && echo "ok $id" || echo "NOSUB $id"
