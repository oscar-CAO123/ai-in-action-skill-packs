/**
 * ingest_performance.ts : agent 1, the internal read. Weekly.
 *
 * What did your own published work actually do, on every channel, over two windows. Reads every
 * published row that can be matched to a platform asset, reads each channel, ranks inside the
 * channel, and writes one snapshot per channel per window onto that row's `performance` array.
 * That column is the only thing this service writes: it never creates a row and never moves a
 * stage.
 *
 * THE RUN IS CONTAINED. Every write goes through guardedWrite. Without ALLOW_PROD_WRITES=1 the
 * payloads print and land in the run directory. Never source a whole environment file into a
 * local run: pass only the variables the run needs.
 *
 *   env -i PATH="$PATH" HOME="$HOME" npx tsx scripts/ingest_performance.ts
 */
import { writeFileSync } from "fs";
import { join } from "path";
import { randomUUID } from "crypto";
import {
  ALLOW_PROD_WRITES, DATA_URL, Gaps, cliFlags, dataSelect, guardedWrite, isoDaysAgo,
  runDirectory, setRunDir, writeHeaders,
} from "./guarded";

// ---------------------------------------------------------------------------
// Your channels. Declare the credential NAME even when you do not have the credential yet: a
// missing one stamps a gap, and turning the channel on later becomes a value, not a code change.
// ---------------------------------------------------------------------------

export const CHANNELS = ["ads_a", "ads_b", "social_a", "social_b", "social_c", "social_d"] as const;
export type Channel = (typeof CHANNELS)[number];

const PAID: ReadonlySet<Channel> = new Set<Channel>(["ads_a", "ads_b"]);
const isPaid = (c: Channel) => PAID.has(c);

const CHANNEL_ENV: Record<Channel, string[]> = {
  ads_a: ["ADS_A_TOKEN", "ADS_A_ACCOUNT_ID"],
  ads_b: ["ADS_B_TOKEN", "ADS_B_ACCOUNT_ID"],
  social_a: ["SOCIAL_A_TOKEN"],
  social_b: ["SOCIAL_B_TOKEN"],
  social_c: ["SOCIAL_C_TOKEN"],
  social_d: ["SOCIAL_D_TOKEN"],
};

export interface Window { start: string; end: string }
export interface PlatformAsset { name: string; url: string | null; metrics: Record<string, number> }
export interface ChannelRead { gap: string | null; assets: PlatformAsset[] }

/**
 * One reader per channel. Each returns either a gap or the assets that channel reported in the
 * window. Replace the body with that platform's API call; the shape is all the rest of the run
 * needs.
 */
const READERS: Record<Channel, (w: Window) => Promise<ChannelRead>> = Object.fromEntries(
  CHANNELS.map((c) => [c, async (_w: Window): Promise<ChannelRead> => {
    const missing = CHANNEL_ENV[c].filter((k) => !process.env[k]);
    if (missing.length) return { gap: `${c}: no credential (${missing.join(", ")})`, assets: [] };
    return { gap: `${c}: reader not implemented yet`, assets: [] };
  }]),
) as Record<Channel, (w: Window) => Promise<ChannelRead>>;

// ---------------------------------------------------------------------------

export interface Snapshot {
  channel: Channel;
  window_start: string;
  window_end: string;
  metrics: Record<string, number>;
  rank: number | null;
  ref: string;
}

interface PublishedRow {
  id: string;
  title: string;
  asset_code: string | null;
  platform_refs: Record<string, string> | null;
  performance: Snapshot[] | null;
}

const MAX_SNAPSHOTS_PER_ROW = 48;
const TABLE = process.env.CONTENT_TABLE || "ContentItem";

/** The metric each channel is ranked on. Ranking across channels compares unlike things. */
const RANK_METRIC: Record<Channel, string> = {
  ads_a: "cost_per_result", ads_b: "cost_per_result",
  social_a: "views", social_b: "views", social_c: "views", social_d: "impressions",
};

const LOWER_IS_BETTER: ReadonlySet<string> = new Set(["cost_per_result", "cost_per_click"]);

/** Two windows ending yesterday, so a piece can win the week and lose the month. */
function windows(): Window[] {
  const end = isoDaysAgo(1);
  return [{ start: isoDaysAgo(7), end }, { start: isoDaysAgo(28), end }];
}

/** Reduce a post URL to the id both sides can agree on. */
export function urlKey(url: string | null): string | null {
  if (!url) return null;
  const m = url.match(/([A-Za-z0-9_-]{8,})\/?(?:\?|$)/);
  return m ? m[1] : null;
}

/**
 * Paid matches on the asset code carried in the ad name. Organic matches on the URL a person
 * pasted onto the row at publish. Log the match count every run: a count that falls to zero is
 * the alarm that something upstream changed.
 */
export function matchRows(channel: Channel, asset: PlatformAsset, rows: PublishedRow[]): PublishedRow[] {
  if (isPaid(channel)) {
    return rows.filter((r) => r.asset_code && asset.name.includes(r.asset_code));
  }
  const key = urlKey(asset.url ?? asset.name);
  if (!key) return [];
  return rows.filter((r) => urlKey(r.platform_refs?.[channel] ?? null) === key);
}

/** Rank inside the channel, over everything the platform reported. */
export function rankWithinChannel(channel: Channel, snaps: Snapshot[]): void {
  const metric = RANK_METRIC[channel];
  const lower = LOWER_IS_BETTER.has(metric);
  [...snaps]
    .sort((a, b) => {
      const x = a.metrics[metric] ?? 0, y = b.metrics[metric] ?? 0;
      return lower ? x - y : y - x;
    })
    .forEach((s, i) => { s.rank = i + 1; });
}

/** Merge by channel plus window, so a re-run corrects a snapshot rather than duplicating it. */
export function mergeSnapshots(existing: Snapshot[] | null, incoming: Snapshot[]): Snapshot[] {
  const out = Array.isArray(existing) ? [...existing] : [];
  for (const s of incoming) {
    const i = out.findIndex((x) =>
      x.channel === s.channel && x.window_start === s.window_start && x.window_end === s.window_end);
    if (i === -1) out.push(s); else out[i] = s;
  }
  out.sort((a, b) => a.window_start.localeCompare(b.window_start));
  return out.slice(-MAX_SNAPSHOTS_PER_ROW);
}

async function main() {
  const runId = `ingest-${new Date().toISOString().slice(0, 10)}-${randomUUID().slice(0, 8)}`;
  setRunDir(join(process.env.RUN_ARTIFACTS_DIR || ".artifacts", "runs", runId));
  console.log(`run ${runId}`);
  const gaps = new Gaps();
  const { flag } = cliFlags();

  let rows = await dataSelect<PublishedRow>(
    `${TABLE}?select=id,title,asset_code,platform_refs,performance&stage=eq.published&is_archived=eq.false`);
  const only = flag("only", "");
  if (only) rows = rows.filter((r) => r.id === only || r.asset_code === only);
  const matchable = rows.filter((r) => r.asset_code || Object.keys(r.platform_refs ?? {}).length);
  console.log(`published rows: ${rows.length}, matchable: ${matchable.length}`);
  if (!rows.length) gaps.stamp("no rows read: the channel reads still run and print");

  const perRow = new Map<string, Snapshot[]>();
  const report: Record<string, { gap: string | null; assets: number; matched: number }> = {};

  for (const w of windows()) {
    for (const channel of CHANNELS) {
      const read = await READERS[channel](w);
      const key = `${channel}@${w.start}..${w.end}`;
      if (read.gap) {
        gaps.stamp(read.gap);
        report[key] = { gap: read.gap, assets: 0, matched: 0 };
        continue;
      }
      const all: Snapshot[] = read.assets.map((a) => ({
        channel, window_start: w.start, window_end: w.end, metrics: a.metrics, rank: null, ref: "ingest",
      }));
      rankWithinChannel(channel, all);
      let matched = 0;
      read.assets.forEach((a, i) => {
        for (const row of matchRows(channel, a, matchable)) {
          matched++;
          const list = perRow.get(row.id) ?? [];
          list.push({ ...all[i] });
          perRow.set(row.id, list);
        }
      });
      report[key] = { gap: null, assets: read.assets.length, matched };
      console.log(`${key}: ${read.assets.length} assets on the platform, ${matched} matched to rows`);
    }
  }

  let written = 0;
  for (const [id, snaps] of Array.from(perRow.entries())) {
    const row = rows.find((r) => r.id === id)!;
    const performance = mergeSnapshots(row.performance, snaps);
    const r = await guardedWrite(
      `patch performance on ${row.asset_code ?? row.title} (${snaps.length} snapshots)`,
      `${DATA_URL}/${TABLE}?id=eq.${id}`,
      {
        method: "PATCH",
        headers: writeHeaders(),
        body: JSON.stringify({ performance, updated_at: new Date().toISOString(), updated_by: "ingest cron" }),
      },
    );
    if (r) written++;
  }

  const summary = {
    run_id: runId,
    ran_at: new Date().toISOString(),
    windows: windows(),
    env_declared: Object.fromEntries(CHANNELS.map((c) =>
      [c, CHANNEL_ENV[c].map((k) => `${k}=${process.env[k] ? "set" : "empty"}`)])),
    report,
    gaps: gaps.list,
    rows_with_snapshots: perRow.size,
    rows_written: written,
    writes_armed: ALLOW_PROD_WRITES,
  };
  writeFileSync(join(runDirectory(), "summary.json"), JSON.stringify(summary, null, 2) + "\n");
  console.log(`\n${perRow.size} rows earned snapshots, ${written} written${ALLOW_PROD_WRITES ? "" : " (writes off)"}; ${gaps.list.length} gaps`);
  console.log(`summary: ${join(runDirectory(), "summary.json")}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
