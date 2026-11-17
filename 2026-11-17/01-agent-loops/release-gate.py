#!/usr/bin/env python3
"""A worked example of a gate: one script that checks a folder of skill files before you share it.

It prints PASS or FAIL per check and exits 0 only when every check passes. Run it on every pass of a
loop, and call the release done only when it exits 0.

    python3 release-gate.py <folder> [<repo root>]

Your private words (company, client and staff names, your own domains) never go in this file. Put
them one per line in a file called .gate-private in the repo root, keep that file out of git, or point
GATE_PRIVATE at it. The gate fails if that list is missing or empty, so a release is never checked
without it.

It reads every file, whatever its type, and every file name. A file it cannot read as text fails.
Lines that state a writing rule ("Never use: ...", "Never write ...") are skipped by the word checks.
A gate catches the mistakes you can name. It does not replace a person reading the release. Known
limits: a key built by joining strings in code, and a bare ~/ or $HOME path, get through.
"""
import os
import re
import sys
import unicodedata
from pathlib import Path

SECRETS = [r"sk-[A-Za-z0-9_-]{20,}", r"sk_(live|test)_[A-Za-z0-9]{16,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
           r"AKIA[0-9A-Z]{16}", r"AIza[0-9A-Za-z_-]{30,}", r"xox[abprs]-[A-Za-z0-9-]{10,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
           r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.",
           r"(?i)(api[_-]?key|secret|token|passw(or)?d)[\"']?\s*[:=]\s*[\"']?[^\s\"'<>{}$]{12,}"]
HOME_PATHS = r"(?i)(/Users/\s*[A-Za-z]|/home/[A-Za-z]|[A-Z]:[\\/]Users[\\/]|%2FUsers%2F|-Users-[A-Za-z])"
BANNED = ["delve", "leverage", "unlock", "seamless", "game-changer", "robust", "elevate"]
NEGATION_SWAP = r"(?i)\b(it'?s|it is|this is|that'?s|that is)( not|n'?t) (just )?[^.]{1,40}[,;:.]\s*(it'?s|it is|this is|that'?s|that is)\b"
EM_DASH = re.compile(r"\u2014|&mdash;|&#8212;|&#x2014;|\\u2014", re.I)
RULE_LINE = re.compile(r"(?i)\bnever (use|write)\b")
ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad"))


def read_all(root):
    texts, unreadable = {}, []
    for p in sorted(root.rglob("*")):
        if p.name == ".git" and p.is_dir():
            unreadable.append(f"{p.relative_to(root)}: a nested .git folder (its history is not checked)")
            continue
        if not p.is_file() or ".git" in p.parts or p.name == ".DS_Store":
            continue
        try:
            raw = p.read_bytes()
        except OSError as e:
            unreadable.append(f"{p.relative_to(root)}: cannot be read ({e.strerror})")
            continue
        for enc in ("utf-8", "utf-16"):
            try:
                t = raw.decode(enc)
                break
            except UnicodeDecodeError:
                t = None
        if t is None or (b"\x00" in raw and not raw.startswith((b"\xff\xfe", b"\xfe\xff"))):
            unreadable.append(f"{p.relative_to(root)}: binary or unknown encoding, check it by hand")
            continue
        texts[p] = unicodedata.normalize("NFKC", t).translate(ZERO_WIDTH)
    return texts, unreadable


def private_words(repo):
    path = Path(os.environ.get("GATE_PRIVATE", repo / ".gate-private"))
    if not path.exists():
        return []
    return [w.strip() for w in path.read_text().splitlines() if w.strip() and not w.startswith("#")]


def squash(s):
    return re.sub(r"[\s_\-.]+", "", s.lower())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).resolve()
    repo = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root.parent
    results = []

    def check(name, problems):
        results.append((name, problems))

    texts, unreadable = read_all(root) if root.is_dir() else ({}, [])
    me = Path(__file__).resolve()
    texts = {p: ("" if p.resolve() == me else t) for p, t in texts.items()}  # its own patterns would match themselves
    rel = {p: str(p.relative_to(root)) for p in texts}
    check("files found", [] if texts else [f"no readable files under {root}"])
    check("every file readable as text", unreadable)

    # Each file is scanned as written, joined across line breaks, and by its own path.
    views = {p: (t, t.replace("\n", "").replace("\r", ""), rel[p]) for p, t in texts.items()}
    check("secrets", [f"{rel[p]}: matches {pat[:24]}" for p, vs in views.items() for pat in SECRETS if any(re.search(pat, v) for v in vs)])
    check("private paths", [f"{rel[p]}: {m.group(0)}" for p, vs in views.items() for v in vs[:1] + vs[2:] for m in [re.search(HOME_PATHS, v)] if m])

    words = private_words(repo)
    if not words:
        check("private words", ["no private words to check: add them to .gate-private (or set GATE_PRIVATE)"])
    else:
        hits = set()
        for p, (t, joined, name) in views.items():
            body = squash(t) + "|" + squash(name)
            for i, w in enumerate(words, 1):
                if squash(w) and squash(w) in body:
                    hits.add(f"{rel[p]}: a private word (line {i} of the list)")
        check("private words", sorted(hits))

    check("em dashes", [rel[p] for p, t in texts.items() if EM_DASH.search(t) and p.suffix not in {".py", ".mjs", ".js"}]
          + [rel[p] for p, t in texts.items() if "\u2014" in t and p.suffix in {".py", ".mjs", ".js"}])
    prose = {p: "\n".join(l for l in t.splitlines() if not RULE_LINE.search(l)) for p, t in texts.items()
             if p.suffix.lower() in {".md", ".txt", ".html"}}
    check("banned words", [f"{rel[p]}: {w}" for p, t in prose.items() for w in BANNED if re.search(r"(?i)\b" + w + r"\b", t)])
    check("negation swap", [rel[p] for p, t in prose.items() if re.search(NEGATION_SWAP, t)])

    fm = []
    for p, t in texts.items():
        if p.suffix.lower() != ".md" or (p.name.lower() != "skill.md" and not t.startswith("---")):
            continue
        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
        if not m or not re.search(r"^name:\s*\S", m.group(1), re.M) or not re.search(r"^description:\s*\S", m.group(1), re.M):
            fm.append(f"{rel[p]}: needs frontmatter with name and description")
    check("skill frontmatter", fm)

    readme = repo / "README.md"
    check("listed in the README", [] if readme.exists() and f"{root.name}/" in readme.read_text(errors="replace") else [f"{root.name}/ is not in {readme.name}"])
    check("drop has a README", [] if (root / "README.md").exists() else ["README.md missing in the drop folder"])

    failed = 0
    for name, problems in results:
        print(f"{'PASS' if not problems else 'FAIL'}  {name}")
        for line in problems[:20]:
            print(f"      {line}")
        failed += bool(problems)
    print(f"\n{len(results) - failed} of {len(results)} checks pass")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
