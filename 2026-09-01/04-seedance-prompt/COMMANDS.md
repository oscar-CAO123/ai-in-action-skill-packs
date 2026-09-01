# L-SEED commands

Canonical commands for the Seedance 2.5 prompt layer. Verified against the CLI on 2026-08-16.
Anything pasted into chat is a preview of this file.

Set these once per session.

```bash
LAYER="path/to/this/skill/folder"
WORK="<the project or idea folder for this shot>"
PROMPT="$WORK/prompt.txt"        # the seven blocks, written first, never inline
REF1="$WORK/ref1.png"            # your reference still
REF2="$WORK/ref2.png"            # optional
```

## 0. Inspect the model (free)

```bash
higgsfield model get seedance_2_5
```

## 1. Cost it before creating it (free, spends nothing)

Same flags as `create`. Local paths auto-upload, so this also confirms the references are readable.

```bash
higgsfield generate cost seedance_2_5 \
  --prompt "$(cat "$PROMPT")" \
  --mode omni_reference \
  --image-references "$REF1" \
  --aspect-ratio 9:16 \
  --duration 10 \
  --resolution 1080p \
  --generate-audio false
```

## 2. One paid generation (STOP after this until you have reviewed it)

```bash
higgsfield generate create seedance_2_5 \
  --prompt "$(cat "$PROMPT")" \
  --mode omni_reference \
  --image-references "$REF1" \
  --aspect-ratio 9:16 \
  --duration 10 \
  --resolution 1080p \
  --generate-audio false \
  --bitrate-mode high \
  --wait --wait-timeout 20m --wait-interval 10s
```

Two references, each with its own job stated in `[REFERENCES]`:

```bash
  --image-references "$REF1" --image-references "$REF2"
```

Landing on a known frame, or looping:

```bash
  --end-image "$WORK/end.png"
```

`start_image` is literally frame one of the render. Only pass it when the still is meant to open
the shot.

## 3. Verify the return is silent

```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$WORK/out.mp4"
```

One `video` line and no `audio` line. If an audio stream came back, strip it and re-check:

```bash
ffmpeg -i "$WORK/out.mp4" -c:v copy -an "$WORK/out-silent.mp4"
```

## 4. Look at the return before reporting

```bash
mkdir -p "$WORK/frames"
ffmpeg -v error -i "$WORK/out.mp4" -vf "fps=2" "$WORK/frames/f_%03d.png"
```

Read the frames. A clean exit code is not a reviewed shot.
