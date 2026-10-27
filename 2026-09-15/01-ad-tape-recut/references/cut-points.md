# Why the cut points land where they do

A hard cut on a segment timecode fails three ways on to-camera footage with burned-in captions.

1. **The caption is mid-swap.** The caption band changes a few frames before or after the word
   starts. Cut on the word and the first frame shows the previous caption, so the viewer reads a
   line the speaker is not saying. Fix: find the caption-change frames once per film (a scene
   change detector over the caption band only, `crop=W:H:0:Y`, threshold 0.05) and snap the start
   to the swap that brings the first word's caption up, as long as that swap is after the previous
   word ended.
2. **The sentence is unfinished.** The user picks segment ends by meaning, not by full stops. Whisper
   gives punctuation on the last word of a sentence. If the requested end falls before the full
   stop, run forward to it (up to 0.8 s). If no full stop is close ahead, trim back to the last one
   (up to 2.5 s). If neither, keep the requested end and write WARNING in the cut list, because the
   user will want to hear those first.
3. **The join clicks.** Two parts butted together at zero crossing luck click or thump. A 30 ms fade
   in and out on every part's audio removes it without being audible as a fade.

Two more things the cutter does:

- **Silence gaps corroborate.** `silencedetect` at -32 dB over 120 ms gives the pauses. An end that
  lands inside a pause is noted. An end that lands inside speech is the thing to look at.
- **Contiguous parts merge.** If the next segment starts within 0.35 s of where the last one ended
  in the same film, they become one range and one snap, so a native run of a film stays one take.

The encode is one ffmpeg pass: per part `-ss` and `-to` on the input, scale to 720x1280 at 30 fps,
`setpts=PTS-STARTPTS`, audio to 44.1 kHz stereo with the fades, then `concat`. H.264 CRF 18,
AAC 192k, `+faststart`.
