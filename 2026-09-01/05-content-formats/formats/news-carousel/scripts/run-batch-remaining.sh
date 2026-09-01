#!/bin/bash
# Finish the noir pain-carousel batch: staff slide 1 (3rd attempt) + hiring 4-6 + 7 unstarted decks.
# 45 plates, ~90 credits. Existing plates are SKIPPED, so this is safe to re-run after a kill.
cd "$(dirname "$0")" || exit 1

echo "=== noir-pain-staff slide 1 (v3) ==="
python3 plates_noir.py noir-pain-staff 1

for s in noir-pain-hiring noir-pain-marketing noir-pain-security noir-pain-lockin \
         noir-pain-governance noir-pain-execution-gap noir-pain-cx noir-pain-roster; do
  echo "=== $s ==="
  python3 plates_noir.py "$s"
done

echo "=== BATCH COMPLETE ==="
