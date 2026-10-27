-- 001-content-workspace.sql
-- Additive only. Read it, run it, keep the file, and write 001-REVERSE.md before you apply it.
-- No drop, no alter type, no rename, and no framework migration tool against real rows.

-- The batch: one run of the machine, usually one week. Every card on the board files under this.
create table if not exists "ContentBatch" (
  id           uuid primary key default gen_random_uuid(),
  week_of      date        not null,
  lane         text        not null default 'default',
  summary      text,
  created_at   timestamptz not null default now()
);

-- The content row: identity, process, formula, evidence. Flat. A variant is a row that shares a
-- concept_code, never a child table.
alter table "ContentItem" add column if not exists stage          text not null default 'ideas';
alter table "ContentItem" add column if not exists batch_id       uuid references "ContentBatch"(id);
alter table "ContentItem" add column if not exists concept_code   text;
alter table "ContentItem" add column if not exists asset_code     text;
alter table "ContentItem" add column if not exists is_archived    boolean not null default false;

-- The formula, one column each because the board filters on them.
alter table "ContentItem" add column if not exists avatar         text;
alter table "ContentItem" add column if not exists pain           text;
alter table "ContentItem" add column if not exists format_id      text;
alter table "ContentItem" add column if not exists asset_class    text;   -- static | carousel | video
alter table "ContentItem" add column if not exists surface        text;   -- organic | paid

-- The working fields the editor window writes.
alter table "ContentItem" add column if not exists hook           text;
alter table "ContentItem" add column if not exists shot_spec      jsonb;
alter table "ContentItem" add column if not exists reference_urls jsonb;
alter table "ContentItem" add column if not exists thumbnail_url  text;

-- The evidence. performance is written only by the internal read agent, platform_refs only by a
-- person at publish, evidence only by the ideation agent.
alter table "ContentItem" add column if not exists performance    jsonb;  -- [{channel, window_start, window_end, metrics, rank, ref}]
alter table "ContentItem" add column if not exists platform_refs  jsonb;  -- {channel: post_url}
alter table "ContentItem" add column if not exists evidence       jsonb;

alter table "ContentItem" add column if not exists updated_at     timestamptz not null default now();
alter table "ContentItem" add column if not exists updated_by     text;

-- The board reads by stage constantly, the crons read by asset code, the podium by concept.
create index if not exists content_stage_idx      on "ContentItem" (stage) where is_archived = false;
create index if not exists content_batch_idx      on "ContentItem" (batch_id);
create index if not exists content_asset_code_idx on "ContentItem" (asset_code);
create index if not exists content_concept_idx    on "ContentItem" (concept_code);

-- The market read from agent 2 lives in its own table, deduplicated on the source URL.
create table if not exists "MarketSignal" (
  id           uuid primary key default gen_random_uuid(),
  source       text        not null,
  source_url   text        not null unique,
  title        text,
  captured_at  timestamptz not null default now(),
  verdict      jsonb
);

-- Stages stay text on purpose. You will rename one in month two, and an enum makes that a
-- migration. The vocabulary lives in one file the app and the crons both import:
--   ideas | ready_to_produce | produced | scheduled | published
