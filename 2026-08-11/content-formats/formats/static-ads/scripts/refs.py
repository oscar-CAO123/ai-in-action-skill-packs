#!/usr/bin/env python3
"""The reference resolver for house content. Every generation cites what it is modelled on.

    python3 refs.py                      # every bank, with counts
    python3 refs.py list hook            # the ids in one bank
    python3 refs.py show arch:S6         # the entry, verbatim
    python3 refs.py show swipe:09 --open # ... and open the image in Preview
    python3 refs.py check arch:S6 hook:S1 style:noir-oil   # exit 1 if any id is dead

the operator's law, 2026-08-10: nothing is generated without a concrete reference from the bank, named
before the generation and shown with it. A reference is an ID that resolves here, not a
description. "modelled on a newspaper" is not a reference; `tpl:Frame 466` is.

The banks are read live off the source files, so there is no second copy of the ids to drift.
Adding an entry to a bank makes it citable immediately, with no edit here.

Banks:
  hook   the copy structure the headline FILLS       references/hooks/HOOKS.md
  arch   the static/video archetype it IMITATES      references/scripts/archetypes.md
  tear   the doctrine the treatment obeys            references/scripts/perdriau-teardowns.md
  hex    the measured shape of the 16-reel corpus    references/transcripts/HEX-CREATIVES-FORMULA.md
  tpl    a Figma layout extract                      context/advertising/static-ads-bank/templates/
  local  a reference image a format was built on     formats/static-ads/references/
  style  a locked plate look                         content-engine/ideas/industry-build-carousels/styles.json
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VAULT = ROOT.parents[5]
house = VAULT / "the business"
REFS = house / "skills" / "content-formats" / "references"
ADS_BANK = house / "context" / "advertising" / "static-ads-bank"
STYLES = (house / "projects" / "content-engine" / "ideas" / "industry-build-carousels"
          / "styles.json")

# bank -> (sources, heading regex). The regex's first group is the id, the second the title.
# `tear` takes a GLOB: teardowns arrive one file per source (Perdriau, then Optamize), and a bank
# that only ever reads one file quietly drops every source added after it.
DOC_BANKS = {
    "hook": (REFS / "hooks" / "HOOKS.md", r"^### ([A-Z]\d+)\. (.+)$"),
    "arch": (REFS / "scripts" / "archetypes.md", r"^## ([A-Z]\d+)\. (.+)$"),
    "tear": (sorted((REFS / "scripts").glob("*teardowns*.md")), r"^## (.+)$"),
    "hex": (REFS / "transcripts" / "HEX-CREATIVES-FORMULA.md", r"^## (.+)$"),
}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def doc_entries(bank):
    """Every heading in a prose bank, with the body that follows it. A bank may be one file or
    several; several are read in order and their entries concatenated."""
    sources, pattern = DOC_BANKS[bank]
    out = []
    for src in (sources if isinstance(sources, list) else [sources]):
        lines = src.read_text().splitlines()
        hits = []
        for n, line in enumerate(lines):
            m = re.match(pattern, line)
            if not m:
                continue
            # Two-group banks carry their own ids (S1, V11). One-group banks get a slug.
            rid, title = ((m.group(1), m.group(2)) if m.lastindex == 2
                          else (slug(m.group(1)), m.group(1)))
            hits.append(dict(id=rid, title=title, line=n, src=src))
        for a, b in zip(hits, hits[1:] + [None]):
            end = b["line"] if b else len(lines)
            a["body"] = "\n".join(lines[a["line"]:end]).rstrip()
        out += hits
    return out


# NOT A BANK, deliberately. the operator, 2026-08-06: the scraped Meta and LinkedIn swipe records were
# moved to `Archive/old-context/static-ads-swipe-banks-2026-08-06/` and are not a source of
# anything. `static-ads/SKILL.md` section 3: "do not re-scrape, do not rebuild them, and do not
# cite them. The reference layer is the 41 Figma extracts and nothing else." A competitor static
# is therefore not citable here, and adding a `swipe` bank back reopens a closed decision.


def image_bank(d, what, recurse=False):
    """Every image in a folder, cited by stem. Stems that collide keep their extension, or
    `image 9` would silently resolve to the .jpg and hide the .png.

    `recurse` walks subfolders and prefixes the id with the folder, so a set extracted from one
    source stays together and cites as `local:optamize-8-statics/03-apology-letter`."""
    if not d.is_dir():
        return []
    it = sorted(d.rglob("*")) if recurse else sorted(d.iterdir())
    files = [f for f in it if f.suffix.lower() in (".png", ".jpg", ".svg", ".webp")]
    stems = [f.stem if f.parent == d else f"{f.parent.name}/{f.stem}" for f in files]
    # `.strip()`: one export is named "VetNotes Static Ads .png", and a trailing space in an id is
    # invisible in a listing and undebuggable in a citation. The gate found it on its first run.
    out = []
    for f, sid in zip(files, stems):
        rid = sid if stems.count(sid) == 1 else f"{sid}{f.suffix}"
        out.append(dict(id=rid.strip(), title=f.name, body=f"{what}: {f.name}", src=f, image=f))
    return out


def tpl_entries():
    return image_bank(ADS_BANK / "templates", "Figma layout extract")


def local_entries():
    return image_bank(ROOT.parent / "references", "Format reference image", recurse=True)


def style_entries():
    if not STYLES.exists():
        return []
    data = json.loads(STYLES.read_text())
    return [dict(id=k, title=(v.get("name") if isinstance(v, dict) else str(k)),
                 body=json.dumps(v, indent=2) if isinstance(v, dict) else str(v),
                 src=STYLES)
            for k, v in data.get("styles", {}).items()]


BANKS = {
    **{b: (lambda b=b: doc_entries(b)) for b in DOC_BANKS},
    "tpl": tpl_entries,
    "local": local_entries,
    "style": style_entries,
}


def resolve(ref):
    """'arch:S6' -> its entry. Raises KeyError with a usable message if it is dead."""
    if ":" not in ref:
        raise KeyError(f"{ref}: a reference is <bank>:<id>, for example arch:S6")
    bank, rid = ref.split(":", 1)
    if bank not in BANKS:
        raise KeyError(f"{ref}: no bank called '{bank}'. Banks: {', '.join(sorted(BANKS))}")
    entries = BANKS[bank]()
    for e in entries:
        if e["id"].lower() == rid.lower():
            return {**e, "bank": bank, "ref": f"{bank}:{e['id']}"}
    # The prose banks slugify their headings, so ids there run long. A UNIQUE prefix resolves,
    # which makes `tear:4` usable; an ambiguous one is an error rather than a coin toss.
    hits = [e for e in entries if e["id"].lower().startswith(rid.lower())]
    if len(hits) == 1:
        return {**hits[0], "bank": bank, "ref": f"{bank}:{hits[0]['id']}"}
    if len(hits) > 1:
        raise KeyError(f"{ref}: matches {len(hits)} ids: "
                       + ", ".join(f"{bank}:{e['id']}" for e in hits[:4]))
    raise KeyError(f"{ref}: '{rid}' is not in the {bank} bank. Run: refs.py list {bank}")


def line_of(entry):
    """Where the entry lives, as a path the reader can open."""
    n = entry.get("line")
    return f"{entry['src']}" + (f":{n + 1}" if n is not None else "")


def cmd_show(args):
    ref = args[0]
    e = resolve(ref)
    print(f"{e['ref']}  {e['title']}")
    print(line_of(e))
    print()
    print(e["body"])
    if "--open" in args:
        target = e.get("image") or e["src"]
        subprocess.run(["open", "-a", "Preview" if e.get("image") else "Cursor", str(target)])


def cmd_list(args):
    banks = args or sorted(BANKS)
    for b in banks:
        entries = BANKS[b]()
        print(f"\n=== {b}  ({len(entries)}) ===")
        for e in entries:
            print(f"  {b}:{e['id']:<28} {e['title']}")


def cmd_check(args):
    dead = []
    for ref in args:
        try:
            e = resolve(ref)
            print(f"  ok    {e['ref']:<24} {e['title']}")
        except KeyError as err:
            dead.append(str(err))
            print(f"  DEAD  {ref}")
    if dead:
        print("\n" + "\n".join(dead))
        sys.exit(1)
    print("\nclean")


def main():
    argv = sys.argv[1:]
    if not argv:
        total = 0
        for b in sorted(BANKS):
            n = len(BANKS[b]())
            total += n
            src = DOC_BANKS[b][0] if b in DOC_BANKS else {"tpl": ADS_BANK / "templates",
                                                          "local": ROOT.parent / "references",
                                                          "style": STYLES}[b]
            # `tear` is a glob, so its source is a list of files rather than one path.
            where = (", ".join(str(p.relative_to(VAULT)) for p in src)
                     if isinstance(src, list) else str(src.relative_to(VAULT)))
            print(f"  {b:<7} {n:>4}  {where}")
        print(f"\n  {total} citable references. refs.py list <bank> to see them.")
        return
    cmd, args = argv[0], argv[1:]
    try:
        {"show": cmd_show, "list": cmd_list, "check": cmd_check}[cmd](args)
    except KeyError as err:
        # A dead id is an ordinary answer here, not a crash. Print it and exit 1 so a caller
        # can gate on it without reading a traceback.
        print(str(err).strip('"'))
        sys.exit(1)


if __name__ == "__main__":
    main()
