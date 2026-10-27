#!/usr/bin/env python3
"""Build a context-transfer repository from a business's brain folder, driven by a JSON manifest.
Usage: python3 build_transfer.py transfer.json

Wipes the clone's working tree (never .git), copies every file the manifest includes, redacts
phone numbers and personal email addresses in the copies, stops on anything that looks like a key
or token, writes README.md, CLAUDE.md, AGENTS.md (the router) and INGEST.md, prints what it did.
Never commits, never pushes. Text only: the manifest's include globs decide, and anything over
`max_file_bytes` is skipped."""
import json, re, shutil, sys, subprocess
from pathlib import Path

SECRET = re.compile(r"(sk-[A-Za-z0-9]{10,}|gho_[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{12,}|eyJ[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}|secret\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}|token\s*[:=]\s*['\"]?[A-Za-z0-9_-]{20,})", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def main(manifest_path, yes=False):
    mp = Path(manifest_path)
    if not mp.exists(): sys.exit(f"manifest not found: {mp} (the path is relative to where you run this)")
    m = json.loads(mp.read_text())
    for key in ("business_name", "source_root", "repo_path", "include_globs"):
        if key not in m: sys.exit(f"manifest is missing '{key}'")
    V = Path(m["source_root"]).expanduser(); R = Path(m["repo_path"]).expanduser()
    if not V.is_dir(): sys.exit(f"source_root not found: {V}")
    if not (R / ".git").is_dir(): sys.exit(f"repo_path is not a git clone: {R}")
    exclude = re.compile("|".join(m.get("exclude_patterns", [])) or r"(?!x)x", re.I)
    ok_email = re.compile("|".join(re.escape(d) + "$" for d in m.get("allowed_email_domains", [])) or r"(?!x)x", re.I)
    # conservative by default: a country code or a leading zero, then digit groups with optional
    # spaces or dashes. Years, prices and order numbers do not match. Override per business.
    phone = re.compile(m.get("phone_pattern", r"(?<![\w.-])(?:\+\d{1,3}[ -]?\(?\d{1,4}\)?|0\d{1,4})(?:[ -]?\d{2,4}){2,3}(?![\w-])"))
    max_bytes = int(m.get("max_file_bytes", 400_000))
    existing = [p for p in R.iterdir() if p.name != ".git"]
    if existing:
        print(f"About to clear {len(existing)} top-level entries in {R} (everything except .git). Commit anything you want to keep first.")
        if not yes and input("Continue? [y/N] ").strip().lower() != "y": sys.exit("stopped, nothing changed")
    for p in existing:
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    files = {}
    for pat in m["include_globs"]:
        for f in sorted(V.glob(pat)):
            rel = f.relative_to(V).as_posix()
            if not f.is_file() or f.name.startswith(".") or exclude.search(rel + "/") or f.stat().st_size > max_bytes: continue
            files[rel] = f
    if not files: sys.exit("no files matched the include globs; nothing written (run `git checkout .` in the clone to restore what was cleared)")
    secrets, redactions = [], []
    for rel, src in files.items():
        try: txt = src.read_text()
        except UnicodeDecodeError: print(f"  skipped (binary): {rel}"); continue
        for hit in SECRET.finditer(txt): secrets.append((rel, hit.group(0)[:10] + "…"))
        txt, np_ = phone.subn("[phone redacted]", txt)
        ne = sum(1 for x in EMAIL.finditer(txt) if not ok_email.search(x.group(0)))
        txt = EMAIL.sub(lambda x: x.group(0) if ok_email.search(x.group(0)) else "[email redacted]", txt)
        if np_ or ne: redactions.append((rel, np_, ne))
        dst = R / rel; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_text(txt)
    if secrets:
        print(f"STOP: {len(secrets)} things that look like keys or tokens. Nothing is committed. Fix the source or exclude the file:")
        for rel, hit in secrets: print(f"  {rel}  {hit}")
        sys.exit(1)
    biz = m["business_name"]; tree = "\n".join(f"- `{k}`" for k in files)
    (R / "README.md").write_text(f"""# Agent context transfer: {biz}

The core documentation and skill files of {biz}, copied from the brain folder so every agent reads
the same files. Text only. No secrets, no customer, client or candidate records, no PDFs.

**An agent pointed at this repository for the first time reads `INGEST.md`** and follows the
ingestion half of the `agent-context-transfer` skill: discover, inventory, build the skills
natively, map the context, plan the orchestrator, verify. Otherwise start at `CLAUDE.md`.

## What is in here ({len(files)} files)

{tree}

## Refresh

`python3 build_transfer.py transfer.json` rebuilds this tree from the brain folder and scans it.
Review `git diff`, commit, push after you have looked.
""")
    router = f"""# {biz}: agent context router

You are reading the transferred core documentation of {biz}. Every file is text copied from the
business's brain folder; the paths mirror that folder, so a reference in one file resolves to
another file here or is deliberately absent (secrets, records, binaries).

## First session here

Read `INGEST.md`, then run the ingestion half of the `agent-context-transfer` skill. Every later
session starts from `_native/context-map.md` if it exists.

## Read in this order

{chr(10).join(f"{i}. `{p}`" for i, p in enumerate(m.get("read_order") or ["README.md"], 1))}

## Rules that bind here

{chr(10).join("- " + r for r in m.get("rules", []))}
- Nothing in this repository is a secret and none may be added.
- Records (customers, clients, candidates, proposals, meetings) are not here by design; ask, never invent.
- Read-only by default: an agent working from this repository drafts, it never sends, posts or deploys.
"""
    (R / "CLAUDE.md").write_text(router); (R / "AGENTS.md").write_text(router)
    ingest = (Path(__file__).resolve().parent.parent / "templates" / "INGEST.md").read_text()
    (R / "INGEST.md").write_text(ingest.replace("{{BUSINESS}}", biz).replace("{{TREE}}", "\n".join("- " + l for l in m.get("tree_notes", []))))
    (R / ".gitignore").write_text(".DS_Store\n.env\n.env.*\n*.pem\n_native/\n")
    print(f"{len(files)} files copied into {R}; scan clean")
    for rel, np_, ne in redactions: print(f"  redacted {np_} phones, {ne} emails in {rel}")
    print(subprocess.run(["git", "-C", str(R), "status", "--short"], capture_output=True, text=True).stdout[-2000:])

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else "transfer.json", yes="--yes" in sys.argv)
