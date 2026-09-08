# Reverse for 001-content-workspace.sql

Written before the change was applied, which is the only time it gets written honestly.

Every statement in `001-content-workspace.sql` is additive, so the reverse is a drop of exactly
what it added and nothing else. Run it only if the workspace is being abandoned: dropping a column
takes its data with it.

```sql
drop index if exists content_concept_idx;
drop index if exists content_asset_code_idx;
drop index if exists content_batch_idx;
drop index if exists content_stage_idx;

alter table "ContentItem" drop column if exists updated_by;
alter table "ContentItem" drop column if exists updated_at;
alter table "ContentItem" drop column if exists evidence;
alter table "ContentItem" drop column if exists platform_refs;
alter table "ContentItem" drop column if exists performance;
alter table "ContentItem" drop column if exists thumbnail_url;
alter table "ContentItem" drop column if exists reference_urls;
alter table "ContentItem" drop column if exists shot_spec;
alter table "ContentItem" drop column if exists hook;
alter table "ContentItem" drop column if exists surface;
alter table "ContentItem" drop column if exists asset_class;
alter table "ContentItem" drop column if exists format_id;
alter table "ContentItem" drop column if exists pain;
alter table "ContentItem" drop column if exists avatar;
alter table "ContentItem" drop column if exists is_archived;
alter table "ContentItem" drop column if exists asset_code;
alter table "ContentItem" drop column if exists concept_code;
alter table "ContentItem" drop column if exists batch_id;
alter table "ContentItem" drop column if exists stage;

drop table if exists "MarketSignal";
drop table if exists "ContentBatch";
```

To undo only the batch link while keeping the rest, drop `batch_id` alone and leave every other
column in place. Rows keep their stage and their evidence.
