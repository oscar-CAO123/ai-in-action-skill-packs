# The schema

One table for content, one for batches, one for the market read. Flat rows, additive changes.

## The content row

Identity and process:

| Column | Type | What it is |
|---|---|---|
| `stage` | text, default `ideas` | where the piece is. Text, never an enum. |
| `batch_id` | uuid | the run that proposed it. Every card on the board files under this. |
| `concept_code` | text | `AVATAR-PAIN-FORMAT`, the formula this piece is an instance of. |
| `asset_code` | text | concept code plus a sequence. Minted at produced, locked after, carried in the ad name. |
| `is_archived` | boolean | skip sets this. Nothing deletes. |

The formula fields, one column each rather than a blob, because the board filters on them:
`avatar`, `pain`, `format_id`, `asset_class`, `surface`.

The evidence, as jsonb:

| Column | Shape | Written by |
|---|---|---|
| `performance` | array of snapshots, capped at 48, sorted by window | the internal read agent |
| `platform_refs` | `{ channel: url }` | a person, at publish |
| `evidence` | what the ideation run cited when it proposed this | the ideation cron |

A snapshot is `{ channel, window_start, window_end, metrics, rank, ref }`. `ref` says where it came
from, and `manual` is a legitimate value: a hand-set rank travels as a snapshot so the ranking code
stays single.

## Why performance is a column and not a table

A performance table means a join on every board read, a second migration path, and a second place
for a row to go missing. The array is capped, sorted and merged by channel plus window, so a re-run
corrects a snapshot rather than duplicating it. If you later outgrow this, you will outgrow it with
real data in hand, which is a better position than guessing now.

## The additive discipline

Every schema change is a numbered file with a reverse written at the same time:

```
ops/001-content-columns.sql
ops/001-REVERSE.md
```

- Additive only. `add column if not exists`, and a default where a null would break a read.
- No `drop`, no `alter type`, no rename. A rename is a new column, a backfill, and a cleanup you
  may never need.
- No framework migration tool against a database with real rows in it. Write the SQL, read it, run
  it, keep the file.
- The reverse file says exactly how to undo the change, in SQL, before the change is applied.

## Indexes worth having on day one

```sql
create index if not exists content_stage_idx        on "ContentItem" (stage) where is_archived = false;
create index if not exists content_batch_idx        on "ContentItem" (batch_id);
create index if not exists content_asset_code_idx   on "ContentItem" (asset_code);
create index if not exists content_concept_idx      on "ContentItem" (concept_code);
```

The board reads by stage constantly, the crons read by asset code, and the podium reads by concept.
