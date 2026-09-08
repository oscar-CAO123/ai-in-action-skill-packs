/**
 * guarded.ts : the primitives every scheduled agent in this pack shares.
 *
 * THE CONTAINMENT CONTRACT. Without ALLOW_PROD_WRITES=1 nothing leaves this machine. Every write
 * and every send goes through guardedWrite, which prints the payload and records it under the run
 * directory instead of performing it.
 *
 * Nothing here is tied to one database or one model provider. DATA_URL and DATA_KEY point at
 * whatever REST surface your store exposes; swap sbSelect for your client if you have one.
 *
 * Run a cron locally, contained, with no credentials at all:
 *   env -i PATH="$PATH" HOME="$HOME" npx tsx scripts/ingest_performance.ts
 */
import { mkdirSync, writeFileSync, readFileSync, existsSync } from "fs";
import { join } from "path";

export const DATA_URL = process.env.DATA_URL || "";
export const DATA_KEY = process.env.DATA_KEY || "";
export const ALLOW_PROD_WRITES = process.env.ALLOW_PROD_WRITES === "1";

export const MODEL_REASONING = process.env.MODEL_REASONING || "claude-sonnet-5";

/** Dollars per million tokens. Keep this current; it is the only thing the budget meter trusts. */
export const PRICING: Record<string, { in: number; out: number }> = {
  "claude-sonnet-5": { in: 3, out: 15 },
  "claude-haiku-4-5-20251001": { in: 1, out: 5 },
};

// ---------------------------------------------------------------------------
// The run directory: prompts, checkpoints, would-write payloads, the summary
// ---------------------------------------------------------------------------

let runDir = "";
export function setRunDir(dir: string): void {
  runDir = dir;
  mkdirSync(runDir, { recursive: true });
}
export function runDirectory(): string { return runDir; }

// ---------------------------------------------------------------------------
// THE GATE
// ---------------------------------------------------------------------------

/**
 * The only way a scheduled agent writes or sends anything. It sits directly above fetch.
 *
 * One function, deliberately, rather than a boolean read in four places: a flag that guards the
 * code you remember writing has no reach into a helper somebody else imported. Alerting and
 * monitoring helpers are the usual way a "dry run" writes to production.
 */
export async function guardedWrite(what: string, url: string, init: RequestInit): Promise<Response | null> {
  if (!ALLOW_PROD_WRITES) {
    console.log(`  WOULD ${what} (ALLOW_PROD_WRITES is not 1, so nothing left this machine)`);
    if (runDir) {
      const dir = join(runDir, "would-write");
      mkdirSync(dir, { recursive: true });
      const name = `${Date.now()}-${what.replace(/[^a-z0-9]+/gi, "-").slice(0, 60)}.json`;
      writeFileSync(join(dir, name), JSON.stringify({
        what, url, method: init.method, body: init.body ? JSON.parse(String(init.body)) : null,
      }, null, 2) + "\n");
    }
    return null;
  }
  const r = await fetch(url, init);
  if (!r.ok) throw new Error(`${what} failed ${r.status}: ${(await r.text()).slice(0, 300)}`);
  console.log(`  ${what}: ok`);
  return r;
}

/** Reads are ungated, and they still need a key. With no key you get an empty list and a gap. */
export async function dataSelect<T>(path: string): Promise<T[]> {
  if (!DATA_URL || !DATA_KEY) return [];
  const r = await fetch(`${DATA_URL}/${path}`, {
    headers: { apikey: DATA_KEY, Authorization: `Bearer ${DATA_KEY}` },
  });
  if (!r.ok) throw new Error(`read ${path} failed ${r.status}`);
  return (await r.json()) as T[];
}

export function writeHeaders(prefer = "return=minimal"): Record<string, string> {
  return {
    apikey: DATA_KEY,
    Authorization: `Bearer ${DATA_KEY}`,
    "Content-Type": "application/json",
    Prefer: prefer,
  };
}

// ---------------------------------------------------------------------------
// Gaps: a missing credential is a fact about the run, never a failure
// ---------------------------------------------------------------------------

export class Gaps {
  list: string[] = [];
  stamp(what: string): void {
    this.list.push(what);
    console.log(`  gap: ${what}`);
  }
}

// ---------------------------------------------------------------------------
// The budget meter, above the client
// ---------------------------------------------------------------------------

export class BudgetExceeded extends Error {}

export class Budget {
  spent = 0;
  calls = 0;
  constructor(private cap: number, private runId: string) {}

  /** Four characters a token is close enough to meter against a cap. */
  static estimate(text: string): number { return Math.ceil(text.length / 4); }

  price(model: string, inTokens: number, outTokens: number): number {
    const p = PRICING[model] ?? { in: 3, out: 15 };
    return (inTokens * p.in + outTokens * p.out) / 1_000_000;
  }

  /** Called BEFORE the request, so a stage never starts a call the run cannot afford. */
  reserve(model: string, prompt: string, maxOut: number): void {
    const cost = this.price(model, Budget.estimate(prompt), maxOut);
    if (this.spent + cost > this.cap) {
      throw new BudgetExceeded(
        `run budget of $${this.cap} would be exceeded ($${this.spent.toFixed(2)} spent, this call ` +
        `~$${cost.toFixed(2)}). Checkpoints are intact: resume with --resume ${this.runId}.`,
      );
    }
  }

  record(model: string, inTokens: number, outTokens: number): void {
    this.spent += this.price(model, inTokens, outTokens);
    this.calls++;
  }
}

// ---------------------------------------------------------------------------
// The model call, with the two traps handled
// ---------------------------------------------------------------------------

/**
 * Joins every text block and reads stop_reason.
 *
 * Trap one: a reasoning model can return a thinking block first, so content[0].text is empty and
 * a reader that takes content[0] gets nothing.
 * Trap two: thinking tokens count against max_tokens, so a limit that fitted the previous model
 * truncates on this one, and a truncated reply fails at the JSON parser, which sends you looking
 * in the wrong place.
 */
export function textOf(body: {
  content?: Array<{ type?: string; text?: string }>;
  stop_reason?: string;
  usage?: { input_tokens?: number; output_tokens?: number };
}): string {
  const text = (body.content ?? [])
    .filter((b) => b.type === "text")
    .map((b) => b.text ?? "")
    .join("")
    .trim();
  if (!text || body.stop_reason === "max_tokens" || body.stop_reason === "refusal") {
    throw new Error(
      `no usable text in the reply (stop_reason=${body.stop_reason ?? "none"}, ` +
      `output_tokens=${body.usage?.output_tokens ?? "unknown"}). Raw body is in the run directory.`,
    );
  }
  return text;
}

export async function callModel(
  budget: Budget, model: string, prompt: string, maxOut: number, label: string,
): Promise<string> {
  budget.reserve(model, prompt, maxOut);
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY || "",
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({ model, max_tokens: maxOut, messages: [{ role: "user", content: prompt }] }),
  });
  const body = await r.json();
  if (runDir) writeFileSync(join(runDir, `${label}.raw.json`), JSON.stringify(body, null, 2) + "\n");
  if (!r.ok) throw new Error(`${label} failed ${r.status}`);
  budget.record(model, body?.usage?.input_tokens ?? 0, body?.usage?.output_tokens ?? 0);
  console.log(`  ${label}: stop_reason=${body?.stop_reason}, out=${body?.usage?.output_tokens}`);
  return textOf(body);
}

// ---------------------------------------------------------------------------
// Checkpoints and small shared helpers
// ---------------------------------------------------------------------------

export function saveCheckpoint(stage: string, data: unknown): void {
  if (!runDir) return;
  writeFileSync(join(runDir, `${stage}.json`), JSON.stringify(data, null, 2) + "\n");
}

export function loadCheckpoint<T>(dir: string, stage: string): T | null {
  const p = join(dir, `${stage}.json`);
  return existsSync(p) ? (JSON.parse(readFileSync(p, "utf8")) as T) : null;
}

/** Strips a fence and takes the outermost array, which is what models actually return. */
export const jsonArray = (raw: string): unknown[] => {
  const text = raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
  const a = text.indexOf("["), b = text.lastIndexOf("]");
  if (a === -1 || b === -1) throw new Error("no JSON array in the reply");
  return JSON.parse(text.slice(a, b + 1)) as unknown[];
};

export function isoDaysAgo(days: number, now = Date.now()): string {
  return new Date(now - days * 86_400_000).toISOString().slice(0, 10);
}

/** The week a run belongs to. A week is named by a date, never by a moment. */
export function weekOf(now = new Date()): string {
  const d = new Date(now);
  d.setUTCDate(d.getUTCDate() - d.getUTCDay());
  return d.toISOString().slice(0, 10);
}

export function cliFlags(argv = process.argv.slice(2)) {
  const flag = (name: string, fallback = "") => {
    const i = argv.indexOf(`--${name}`);
    return i === -1 ? fallback : (argv[i + 1] ?? "true");
  };
  return { flag, has: (name: string) => argv.includes(`--${name}`) };
}
