#!/usr/bin/env python3
"""A worked example of a gate: one script that checks a folder of skill files before you share it.

It prints PASS or FAIL per check and exits 0 only when every check passes. Run it on every pass of a
loop, and call the release done only when it exits 0.

    python3 release-gate.py <folder> [<repo root>] [<private word list>]

Your private words (company, client and staff names, your own domains) never go in this file. Put
them one per line in a file called .gate-private in the repo root and keep that file out of git, or
pass the list's path as the third argument. The gate fails if that list is missing or empty, so a
release is never checked without it. It reads no environment variables and makes no network calls.

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

# Every repeat is bounded, so a crafted file cannot make a pattern run for minutes.
SECRETS = [r"sk-[A-Za-z0-9_-]{20,300}", r"sk_(live|test)_[A-Za-z0-9]{16,300}", r"ghp_[A-Za-z0-9]{20,300}", r"github_pat_[A-Za-z0-9_]{20,300}",
           r"AKIA[0-9A-Z]{16}", r"AIza[0-9A-Za-z_-]{30,300}", r"xox[abprs]-[A-Za-z0-9-]{10,300}", r"-----BEGIN [A-Z ]{0,40}PRIVATE KEY-----",
           r"(?i)(api[_-]?key|secret|token|passw(or)?d)[\"']?\s{0,60}[:=]\s{0,60}[\"']?[^\s\"'<>{}$]{12,300}"]
HOME_PATHS = r"(?i)(/Users/\s*[A-Za-z]|/home/[A-Za-z]|[A-Z]:[\\/]Users[\\/]|%2F" + "Users%2F|-Users-[A-Za-z])"
MAX_BYTES = 5_000_000
INVISIBLE = set("\u2800\u3164\u115f\u1160\uffa0")
BANNED = ["delve", "leverage", "unlock", "seamless", "game-changer", "robust", "elevate"]
NEGATION_SWAP = r"(?i)\b(it'?s|it is|this is|that'?s|that is)( not|n'?t) (just )?[^.]{1,40}[,;:.]\s*(it'?s|it is|this is|that'?s|that is)\b"
NEGATION_SWAP_2 = r"(?i)\b(is|are)( not|n'?t) (a |an |the )?[^.,;:]{1,30}[,;:]\s*(the [^.,;:]{1,30} (is|are)|(it|this|that)( is|'s))\b"
EM_DASH = re.compile(r"\u2014|&mdash;?|&#8212;?|&#x2014;?|\\u2014", re.I)
# The writing rule itself names the banned words, so exactly that sentence (and nothing else on its line) is removed
# before the word checks.
RULE_TEXT = re.compile(r"(?i)never use: delve, leverage, unlock, seamless, game-changer, robust, elevate\.|never write \"it's not x, it's y\"\.")
ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad"))


def read_all(root):
    """Every file under root, read as text. Anything that cannot be checked is reported, never skipped."""
    texts, unreadable = {}, []
    paths = []

    def cannot_list(err):
        unreadable.append(f"{safe(Path(err.filename).relative_to(root)) if err.filename else '?'}: folder cannot be read")

    for folder, dirs, files in os.walk(root, onerror=cannot_list, followlinks=False):
        for d in list(dirs):
            full = Path(folder) / d
            if d == ".git" or full.is_symlink():
                what = "a nested .git folder (its history is not checked)" if d == ".git" else "a link to somewhere else, not followed"
                unreadable.append(f"{safe(full.relative_to(root))}: {what}")
                dirs.remove(d)
        paths += [Path(folder) / f for f in files]
    for p in sorted(paths):
        rel = safe(p.relative_to(root))
        if p.name in (".DS_Store", ".git"):
            unreadable.append(f"{rel}: {p.name} should not ship, remove it")
            continue
        if p.is_symlink():
            unreadable.append(f"{rel}: a link to somewhere else, not followed. Replace it with the real file")
            continue
        if not p.is_file():
            unreadable.append(f"{rel}: not a regular file")
            continue
        try:
            if p.stat().st_size > MAX_BYTES:
                unreadable.append(f"{rel}: over {MAX_BYTES // 1_000_000} MB, check it by hand")
                continue
            raw = p.read_bytes()
        except OSError as e:
            unreadable.append(f"{rel}: cannot be read ({e.strerror})")
            continue
        try:
            # UTF-16 only with its byte order mark; everything else must be strict UTF-8.
            t = raw.decode("utf-16") if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else raw.decode("utf-8")
        except UnicodeDecodeError:
            t = None
        if t is None or (b"\x00" in raw and not raw.startswith((b"\xff\xfe", b"\xfe\xff"))):
            unreadable.append(f"{rel}: binary or unknown encoding, check it by hand")
            continue
        texts[p] = clean(t)
    return texts, unreadable


def clean(t):
    """Normalised text: invisible format characters removed, curly quotes made straight."""
    t = unicodedata.normalize("NFKC", t)
    # Invisible format characters, combining marks and blank-looking fillers are removed.
    t = "".join(c for c in t if unicodedata.category(c) not in ("Cf", "Mn", "Me") and c not in INVISIBLE)
    return t.translate({0x2018: "'", 0x2019: "'", 0x02BC: "'", 0x201C: '"', 0x201D: '"', 0x2010: "-", 0x2011: "-"})


def safe(x):
    """A file name printed to the terminal, with control characters shown as escapes."""
    return "".join(c if c.isprintable() else repr(c)[1:-1] for c in str(x))


def private_words(path):
    try:
        if not path.is_file():
            return []
        text = clean(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return []
    return [w.strip() for w in text.splitlines() if w.strip() and not w.startswith("#")]


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
    rel = {p: safe(p.relative_to(root)) for p in texts}
    check("files found", [] if texts else [f"no readable files under {safe(root)}"])
    check("every file readable as text", unreadable)

    # Each file is scanned as written, joined across line breaks, and by its own path.
    views = {p: (t, t.replace("\n", "").replace("\r", ""), rel[p]) for p, t in texts.items()}
    leaks = [f"{rel[p]}: matches {pat[:24]}" for p, vs in views.items() for pat in SECRETS if any(re.search(pat, v) for v in vs)]
    # Web tokens (eyJ...) are found by splitting into word runs once, which stays fast on any input.
    leaks += [f"{rel[p]}: a web token" for p, vs in views.items()
              if any(w.startswith("eyJ") and w.count(".") >= 2 and len(w) > 40 for v in vs for w in re.findall(r"[A-Za-z0-9_.-]+", v))]
    check("secrets", leaks)
    check("private paths", [f"{rel[p]}: a home folder path" for p, vs in views.items() if any(re.search(HOME_PATHS, v) for v in vs[:1] + vs[2:])])

    words = private_words(Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else repo / ".gate-private")
    if not words:
        check("private words", ["no private words to check: add them to .gate-private, or pass a list as the third argument"])
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
    # The rule sentence is cut out and the spacing closed up, so a sentence split around it reads whole again.
    prose = {p: re.sub(r"[ \t]+", " ", RULE_TEXT.sub("", t)) for p, t in texts.items()
             if p.suffix.lower() in {".md", ".markdown", ".txt", ".html", ".htm"}}
    check("banned words", [f"{rel[p]}: {w}" for p, t in prose.items() for w in BANNED if re.search(r"(?i)\b" + w + r"\b", t)])
    check("negation swap", [rel[p] for p, t in prose.items() if re.search(NEGATION_SWAP, t) or re.search(NEGATION_SWAP_2, t)])

    fm = []
    for p, t in texts.items():
        if p.suffix.lower() != ".md" or (p.name.lower() != "skill.md" and not t.startswith("---")):
            continue
        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
        if not m or not re.search(r"^name:\s*\S", m.group(1), re.M) or not re.search(r"^description:\s*\S", m.group(1), re.M):
            fm.append(f"{rel[p]}: needs frontmatter with name and description")
    check("skill frontmatter", fm)

    readme = repo / "README.md"
    try:
        listed = readme.is_file() and f"{root.name}/" in readme.read_text(errors="replace")
    except OSError:
        listed = False
    check("listed in the README", [] if listed else [f"{safe(root.name)}/ is not in the repo README"])
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
