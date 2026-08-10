# Content formats

Twelve production formats for carousels, statics and video, taken out of a working content engine and
stripped back to the craft. Each one is a skill file your agent reads before it builds anything.

These are skeletons on purpose. The house they came from had a locked brand, a hook bank built from
its own scraped corpus, a persona set and a model routing table. All of that came out. What is left
is the part that transfers: how the format is constructed, what makes it fail, and the gates that
stop you paying for a render you are going to throw away.

## What is in here

| Folder | Format | Output |
|---|---|---|
| `formats/static-ads` | The largest one. A bank of single-image ad shapes, plus presentation sub-formats: ruled pad, apology letter, comparison table, inbox, news banner, search sheet, ticked rows, would-you-rather. | Statics |
| `formats/paper-carousel` | Collaged paper sheet, polaroid fan, sculpture end card. | Carousel |
| `formats/permission-carousel` | Period noir, outlined display numerals, copy centred in the band above the subject's head. | Carousel |
| `formats/news-carousel` | Tabloid news-headline construction. | Carousel |
| `formats/industry-build-carousel` | Grid carousel showing what actually gets built, one build per cell. | Carousel |
| `formats/vhs-carousel` | Full-bleed degraded tape frames, type in the negative space. | Carousel |
| `formats/before-after-splitscreen` | Split screen, painted, before and after. | Static or carousel |
| `formats/noir-painterly` | The animation look: oil noir, hand-painted, with an oil-on-paper sub-style. | Video |
| `formats/cutout-story-vo` | Narrated story over painted plates with faceless paper cutouts, hard scale-cuts, a pencil annotation layer. | Video |
| `formats/slide-carousel-vo` | Projector film. One still per point, narrated, word-timed captions. | Video |
| `formats/still-frame-vo` | One cinematic frame, one voiceover. The cheapest video that still looks made. | Video |
| `formats/talkshow-vsl` | Retro talk-show set, long-form sell. | Video |
| `layers/editorial-layer` | A finishing pass: real archival texture fetched and composited. | Layer |
| `layers/path-control` | Drawing a route into a frame and erasing the line as it animates. | Layer |

Most formats ship with their build scripts under `scripts/`. They are ordinary Python and shell, and
they expect ffmpeg and Pillow.

## What came out, and what to put back

Four things were removed because they belong to one business and would make your output look like
theirs:

1. **The brand kit.** Palette, typefaces, aspect specs, the visual do and do-not list.
2. **The hook bank.** A structured library of hook shapes with a rule that hooks are filled from it
   rather than free-written. Worth rebuilding: it is the file that pays back most in the whole engine.
3. **The persona and language rules.** Who the copy is aimed at and the exact words that are and are
   not allowed.
4. **The model routing table.** Which generation model owns which shot type, with verified ids and
   parameters, so nothing gets generated on the wrong one by accident.

Where a skill references `references/` or a config path that is not in this repo, that is one of the
four. Substitute your own file at the same path and the skill runs.

The fastest way to build your own versions is to run the business interview and the funnel builder in
this repo first. Both of them produce the language and the audience definitions these formats want.

## The rules that carry across

These sit inside the format files and they are the reason the output holds up:

- **Approve the still before you animate it.** Motion on a bad frame is a bad frame that moves.
- **Look at the render before you report on it.** A diff of the markup will not show you a clipped
  line or an arrow pointing at nothing.
- **Paid generations one at a time.** Never batch a set you have not seen a single example of.
- **Measure the layout, do not eyeball it.** Where a format says a block centres on something, it
  means measured off the plate, not a fixed position that happens to look right once.
- **A model call is for judgement.** Composition arithmetic is arithmetic. Write the rule.

## Licence

MIT, same as the rest of this repo. Use them commercially, change them, ship them. No attribution
required, though it is welcome.
