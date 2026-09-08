# The workspace

One page, five views, one editor window, over one table.

## Home

The state of the machine in a glance: counts by stage, this week's batch as cover tiles, what is
next on the calendar, and a strip of channels showing which are reporting and which are stamping
gaps. A batch tile opens the batch view scrolled to the piece you clicked.

## Pipeline

The five stages as columns. **Inside each column, one card per batch**, newest first, with a final
card holding work that belongs to no batch. Clicking a batch card opens that batch's pieces at that
stage as a grid.

This is the rule worth keeping. Every version of this board that showed one card per piece became
unusable in about three weeks: two hundred cards in a column, no way to see which week is which,
and a scroll nobody performs. Filing by batch keeps the column the size of a week no matter how
much work accumulates.

The batch grid carries two dropdown filters, format and avatar. Dropdowns rather than chip
rows: chips look better and take a whole row of vertical space to say the same thing.

## The full window

Where a piece is actually worked, opened from any grid.

- **The copy** in a box that grows with the text. A fixed-height textarea for a script is a small
  daily insult.
- **The stage** changed by a control, not by dragging. Dragging is charming and imprecise, and a
  piece that lands in the wrong column silently is worse than one nobody moved.
- **The hook** as its own field, because a piece with no media leads with its hook everywhere in
  the interface.
- **The shot list** as its own field.
- **The references** with an inline viewer, behind the same URL allowlist as your media.
- **The performance snapshots** the crons wrote, and a hand-set rank.

## Concepts

One ranked podium of formulas by how their pieces actually performed, with a channel filter.

A hand-set rank is stored **as a performance snapshot marked `manual`**, so a human judgement and a
measured result travel through the same ranking code. Two ranking paths, one for people and one for
data, drift within a month and then nobody trusts either.

A concept's exemplar is its best ranked piece, chosen automatically. Nobody maintains it.

## Calendar and catalogue

Everything from produced onward. The calendar is what is scheduled and when. The catalogue is
everything ever made, filterable, and it opens the same full window.

## The verbs

Three verbs change what the machine does, and they belong to named people, listed in the server
action:

- **Approve** writes the skeleton of the piece from the idea and moves it forward.
- **Finalise** moves a piece to ready to produce.
- **Skip** archives. It never deletes, because the record of what you decided against is worth
  keeping.

## What not to build

Ratings out of five, sentiment scores, an experiments view, a strategy view. Every one of them was
built, used twice and retired. The row, its stage, its batch and its evidence carry the whole
process.
