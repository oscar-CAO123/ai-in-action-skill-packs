#!/usr/bin/env node
// Email newsletter checker. Plain Node, no dependencies.
// Usage: node check.mjs <file.html>
// Exit 0: no errors (warnings still need reading). Exit 1: at least one error. Exit 2: bad usage.

import { readFileSync } from "node:fs";

// The unsubscribe tag your mailing tool swaps for each recipient's link.
// Change this if your tool uses another name, for example {{unsubscribe}}.
const UNSUB_TOKEN = "{{unsubscribeUrl}}";

const file = process.argv[2];
if (!file) {
  process.stderr.write("usage: node check.mjs <file.html>\n");
  process.exit(2);
}

let html;
try {
  html = readFileSync(file, "utf8");
} catch {
  process.stderr.write(`Could not read ${file}\n`);
  process.exit(2);
}

if (html.length > 400000) {
  process.stderr.write("This file is over 400KB, far too big for an email. Gmail clips anything past about 102KB.\n");
  process.exit(1);
}

const errors = [];
const warnings = [];

// Read one attribute from a tag string. Returns null when the attribute is absent.
function attr(tag, name) {
  const m = new RegExp(`\\s${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)')`, "i").exec(tag);
  return m ? (m[1] ?? m[2] ?? "") : null;
}

// Fixed pixel width of a table, from its width attribute or inline style. 0 when there is none.
function fixedWidth(tag) {
  const w = attr(tag, "width");
  if (w !== null && /^\d+$/.test(w.trim())) return Number(w);
  const css = attr(tag, "style") ?? "";
  const m = /max-width\s*:\s*(\d+)px/i.exec(css) || /(?:^|;)\s*width\s*:\s*(\d+)px/i.exec(css);
  return m ? Number(m[1]) : 0;
}

// Remove every @media block so only the rules outside media queries remain.
function stripMediaBlocks(css) {
  let out = "";
  let i = 0;
  for (;;) {
    const at = css.indexOf("@media", i);
    if (at === -1) return out + css.slice(i);
    out += css.slice(i, at);
    let j = css.indexOf("{", at);
    if (j === -1) return out;
    let depth = 0;
    for (; j < css.length; j++) {
      if (css[j] === "{") depth++;
      else if (css[j] === "}" && --depth === 0) break;
    }
    i = j + 1;
  }
}

// 1. Size. Gmail clips past about 102KB, and the unsubscribe link goes with it.
const bytes = Buffer.byteLength(html, "utf8");
const kb = `${(bytes / 1024).toFixed(1)}KB`;
if (bytes > 102400) errors.push(`The file is ${kb}. Gmail clips past about 102KB. Trim it under 100KB.`);
else if (bytes > 81920) warnings.push(`The file is ${kb}, close to the 102KB clipping point.`);

// 2. No scripts, frames, forms, outside stylesheets or event handlers.
const bannedTags = new Set([...html.matchAll(/<\s*(script|iframe|frame|frameset|object|embed|form|input|button|select|textarea|base|link)\b/gi)].map((m) => m[1].toLowerCase()));
for (const tag of bannedTags) errors.push(`<${tag}> is not allowed in an email. Remove it.`);
const handlers = new Set([...html.matchAll(/<[a-z][^>]{0,2000}>/gi)].flatMap((t) => [...t[0].matchAll(/\s(on[a-z]+)\s*=/gi)]).map((m) => m[1].toLowerCase()));
for (const h of handlers) errors.push(`${h} is an event handler. Email clients strip these. Remove it.`);
if (/@import/i.test(html)) errors.push("@import loads an outside stylesheet, which email clients ignore. Inline the styles.");

// 3. Layout: one 600px container, built from tables.
const tables = [...html.matchAll(/<table\b[^>]{0,2000}>/gi)].map((m) => m[0]);
if (tables.length === 0) errors.push("No table found. Build the layout from tables so it holds in Outlook.");
const widest = Math.max(0, ...tables.map(fixedWidth));
if (tables.length && widest === 0) errors.push("No fixed-width table found. Add a 600px container table.");
else if (widest && widest !== 600) errors.push(`The widest container is ${widest}px. Use 600px.`);
const unmarked = tables.filter((t) => !/role\s*=\s*["']presentation["']/i.test(t)).length;
if (unmarked) errors.push(`${unmarked} table${unmarked === 1 ? "" : "s"} missing role="presentation". Add it to every layout table.`);
if (/position\s*:\s*(fixed|absolute|sticky)/i.test(html)) errors.push("Fixed, absolute or sticky positioning found. Outlook strips it. Use a table instead.");
if (/display\s*:\s*(flex|grid)/i.test(html)) warnings.push("Flexbox or grid CSS found. Outlook ignores it. Use table cells for layout.");

// 4. Styles: inline on each element. The one <style> block holds only media queries.
const css = [...html.matchAll(/<style\b[^>]{0,2000}>([\s\S]{0,200000}?)<\/style>/gi)].map((m) => m[1]).join("\n");
const looseCss = stripMediaBlocks(css).replace(/\/\*[\s\S]*?\*\//g, "").trim();
if (looseCss) errors.push("Style rules sit outside a media query in the <style> block. Move them inline on each element.");
const bareText = [...html.matchAll(/<(td|th|p|h[1-6]|a|span|li)\b[^>]{0,2000}>/gi)].filter((m) => attr(m[0], "style") === null).length;
if (bareText) warnings.push(`${bareText} text element${bareText === 1 ? " has" : "s have"} no inline style. Give each one its own style attribute.`);

// 5. Images: alt text, absolute https address, display block.
const imgs = [...html.matchAll(/<img\b[^>]{0,2000}>/gi)].map((m) => m[0]);
imgs.forEach((tag, n) => {
  const label = `Image ${n + 1}`;
  if (!(attr(tag, "alt") ?? "").trim()) errors.push(`${label} has no alt text. Write a sentence that says what the picture shows.`);
  if (!/^https:\/\//i.test((attr(tag, "src") ?? "").trim())) {
    errors.push(`${label} must use an absolute https:// address. Relative and data: sources do not work in email.`);
  }
  if (!/display\s*:\s*block/i.test(attr(tag, "style") ?? "")) {
    warnings.push(`${label} needs display:block in its style, or Outlook and Gmail leave a gap under it.`);
  }
});

// 6. Links and unsubscribe: a plain text link in the body, not an image or a button.
const anchors = [...html.matchAll(/<a\b([^>]{0,2000})>([\s\S]{0,5000}?)<\/a>/gi)];
const unsub = anchors.filter((m) => (attr(`<a${m[1]}>`, "href") ?? "").includes(UNSUB_TOKEN));
if (!unsub.length) errors.push(`No unsubscribe link. Add <a href="${UNSUB_TOKEN}">Unsubscribe</a> to the footer.`);
else if (!unsub.some((m) => /unsubscribe/i.test(m[2].replace(/<[^>]+>/g, "")))) {
  errors.push("The unsubscribe link has no text that says unsubscribe. Put the word in the link text.");
}
const plainHttp = anchors.filter((m) => /^http:\/\//i.test((attr(`<a${m[1]}>`, "href") ?? "").trim())).length;
if (plainHttp) warnings.push(`${plainHttp} link${plainHttp === 1 ? " uses" : "s use"} http:// rather than https://.`);

// 7. No em dashes, as the character or as an HTML entity.
const emDash = /\u2014|&mdash;|&#8212;|&#x2014;/i;
html.split("\n").forEach((line, n) => {
  if (emDash.test(line)) errors.push(`Em dash on line ${n + 1}. Replace it with a comma, a full stop, a colon or brackets.`);
});

// 8. Document basics.
if (!/<!doctype html/i.test(html)) warnings.push("No <!doctype html> at the top.");
if (!/<meta[^>]{1,2000}charset/i.test(html)) warnings.push('No charset meta. Add <meta charset="utf-8">.');
if (!(/display\s*:\s*none/i.test(html) && /max-height\s*:\s*0/i.test(html))) {
  warnings.push("No hidden preheader found. Add a short hidden line for the inbox preview.");
}

process.stdout.write(`${file}\n`);
process.stdout.write(`  ${kb} of 100KB limit, ${widest ? `${widest}px` : "no fixed"} container, ${imgs.length} image${imgs.length === 1 ? "" : "s"}, ${anchors.length} link${anchors.length === 1 ? "" : "s"}\n`);
for (const e of errors) process.stdout.write(`  ERROR  ${e}\n`);
for (const w of warnings) process.stdout.write(`  warn   ${w}\n`);
if (!errors.length && !warnings.length) process.stdout.write("  clean\n");
process.stdout.write(
  errors.length
    ? `${errors.length} error${errors.length === 1 ? "" : "s"}, ${warnings.length} warning${warnings.length === 1 ? "" : "s"}. Fix the errors.\n`
    : `No errors. ${warnings.length} warning${warnings.length === 1 ? "" : "s"} to read.\n`
);
process.exit(errors.length ? 1 : 0);
