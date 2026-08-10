---
name: lead-magnet-caution-card
description: F7.6.5. The caution card for a lead-magnet static. The canonical news-carousel card with a large drawn hazard triangle or X centred on the plate area. Use when building F-M5 for a new industry. Read formats/static-ads/SKILL.md and lead-magnet/SKILL.md first.
parent: static-ads-lead-magnet
format: F7.6.5
---

# F-M5, the caution card

**Hook 5:** `[Avatar]. Please be careful. Do not touch AI before you do this audit.`
HOOKS.md: **S2** negative / problem call-out, opened with **P5**.

The canonical news-carousel card: plate y0 to 844, band y844 to 1350, `noir` theme, **ALL CAPS**.

## Build

```
python3 build_caution.py <industry>
# only if that industry has no plate on disk:
python3 plates_magnet.py <industry> caution --go     # ONE paid job
```

**Free for any industry whose VHS plate is already shot.** Five of the seven reuse a keeper plate
from `news-carousel/scripts/plates-real/`; Building Services and Professional Services need one
each.

## The law

**This is the one format in the lead-magnet set that keeps caps**, because it IS the
news-carousel format and it is the control the other four are judged against. `band.py` applies
the transform, so the copy string is not pre-cased.

**The mark is centred on the PLATE AREA, not the card.** `CX, CY = W/2, PLATE_H/2`, so y=422 and
not the card's own 675. the operator, 2026-08-06.

**Large, centred, symmetrical, and no laptop.** The first pass drew a laptop with a small hazard
sign over it; the operator cut the laptop entirely and scaled the mark up.

**Per-mark scale, not one shared number.** The triangle's local box is 156 units tall and the X's
is 192, so a shared scale draws the X a quarter larger: it ran into the magnet label at the foot
of the plate and touched the top edge. `MARK_SCALE` lands both at the same 530px optical height.

**The emblem is DRAWN, never generated.** A model asked for a hazard sign over a device returns a
warped sign with invented lettering on it, and the plate underneath is already paid for.

## The recorded deviation

the operator cut the leader-arrow annotation off the industry statics on 2026-08-06, which put those
cards under "nothing is drawn over the plate". **This card draws over the plate on purpose**: the
caution mark across the frame is the whole format. The magnet rides underneath it as a plain
centred label with no leader line, which is the lightest way to name the asset without reviving
the arrow.

## Casting

`LOOK` alternates `hazard` and `cross` across the seven industries, so the set does not read as
one mark repeated. That is the only thing that varies between cards.
