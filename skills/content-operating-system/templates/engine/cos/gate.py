"""The batch gate.

A batch is not finished because it looks finished. It is finished because this exited clean.

The gate enforces the mechanical half only: traceability, proof tiers, banned language, format
compliance, and files that actually exist. The judgement half stays with a person. The gate
exists so the person spends their attention on judgement instead of on catching typos.

    python3 -m cos.gate outputs/drafts/2026-09-01/batch.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import config as config_module

EM_DASH = re.compile(r"[—–]")
NEGATION_SWAP = re.compile(
    r"\b(?:it'?s|this is|that'?s|they'?re|we'?re|you'?re)\s+not\s+[^.,;!?]{2,60}[,.]?\s*"
    r"(?:it'?s|this is|that'?s|they'?re|we'?re|you'?re)\s+",
    re.IGNORECASE,
)
NEGATION_SWAP_SHORT = re.compile(r"\bless\s+\w+[,.]?\s+more\s+\w+", re.IGNORECASE)

BANNED = [
    "leverage", "leveraging", "seamless", "seamlessly", "navigate the", "empower", "empowering",
    "unlock", "unlocking", "harness", "harnessing", "game-changing", "game changer",
    "revolutionary", "revolutionise", "revolutionize", "cutting-edge", "transformative",
    "robust", "synergy", "supercharge", "next-generation", "next-gen", "paradigm shift",
    "the future of", "this changes everything", "level up", "delve", "tapestry", "testament to",
    "in today's fast-paced", "in the age of ai", "as ai continues", "the ai revolution",
    "ai-powered", "must-have", "must-read", "the only way", "the best way", "you won't believe",
    "let's dive in", "buckle up", "in conclusion", "it's worth noting",
]

TIERS = {"shown", "quoted", "held"}


def load_extra_bans(root: Path) -> list[str]:
    """Pick up the operator's own bans from brain/language-rules.md."""
    path = root / "brain" / "language-rules.md"
    if not path.exists():
        return []
    extra = []
    for line in path.read_text().splitlines():
        match = re.match(r"^-\s+banned:\s*(.+)$", line.strip(), re.IGNORECASE)
        if match:
            extra.extend(w.strip().lower() for w in match.group(1).split(",") if w.strip())
    return extra


def copy_fields(asset: dict) -> list[tuple[str, str]]:
    out = []
    for key in ("hook", "angle", "script", "caption", "body", "subject", "close"):
        value = asset.get(key)
        if isinstance(value, str) and value.strip():
            out.append((key, value))
    for index, slide in enumerate(asset.get("slides", []) or []):
        if isinstance(slide, str):
            out.append((f"slides[{index}]", slide))
        elif isinstance(slide, dict):
            for key, value in slide.items():
                if isinstance(value, str) and value.strip():
                    out.append((f"slides[{index}].{key}", value))
    return out


def check_asset(asset: dict, cfg: dict, root: Path, bans: list[str],
                queue_ids: set[str]) -> list[str]:
    name = asset.get("id") or asset.get("file") or "unnamed asset"
    fails: list[str] = []

    idea_id = asset.get("idea_id")
    if not idea_id:
        fails.append(f"{name}: no idea_id")
    elif queue_ids and idea_id not in queue_ids:
        fails.append(f"{name}: idea_id '{idea_id}' is not in any queue file")

    fmt = asset.get("format")
    if not fmt:
        fails.append(f"{name}: no format")
    elif cfg.get("formats") and fmt not in cfg["formats"]:
        fails.append(f"{name}: format '{fmt}' is not a selected format")
    elif not (root / "brain" / "formats" / f"{fmt}.md").exists():
        fails.append(f"{name}: brain/formats/{fmt}.md does not exist")

    tier = asset.get("proof_tier")
    if tier not in TIERS:
        fails.append(f"{name}: proof_tier must be one of {sorted(TIERS)}, got {tier!r}")
    if tier == "held" and not asset.get("framed_as_position"):
        fails.append(f"{name}: a 'held' claim must set framed_as_position true")
    if tier == "quoted" and not asset.get("evidence"):
        fails.append(f"{name}: a 'quoted' claim needs at least one evidence record id")

    if asset.get("hook") and not asset.get("hook_structure"):
        fails.append(f"{name}: hook has no hook_structure id (the citation law)")

    for field, text in copy_fields(asset):
        lowered = text.lower()
        if EM_DASH.search(text):
            fails.append(f"{name}.{field}: em dash")
        if NEGATION_SWAP.search(text) or NEGATION_SWAP_SHORT.search(text):
            fails.append(f"{name}.{field}: negation swap")
        for word in BANNED + bans:
            if word in lowered:
                fails.append(f"{name}.{field}: banned phrase '{word}'")

    for key in ("file", "thumbnail", "audio"):
        ref = asset.get(key)
        if ref and not (root / ref).exists():
            fails.append(f"{name}.{key}: file does not exist: {ref}")

    return fails


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 -m cos.gate <batch.json>")
        return 2

    batch_path = Path(sys.argv[1])
    if not batch_path.exists():
        print(f"no batch at {batch_path}")
        return 2

    config_module.load_dotenv()
    cfg = config_module.load()
    root = Path(cfg["_root"])
    bans = load_extra_bans(root)

    queue_ids: set[str] = set()
    for queue_file in (root / "outputs" / "queue").glob("*/queue.json"):
        try:
            data = json.loads(queue_file.read_text())
        except json.JSONDecodeError:
            continue
        for idea in data.get("ideas", []):
            queue_ids.add(str(idea.get("id") or idea.get("rank")))

    batch = json.loads(batch_path.read_text())
    assets = batch if isinstance(batch, list) else batch.get("assets", [])
    if not assets:
        print("batch has no assets")
        return 2

    fails: list[str] = []
    for asset in assets:
        fails.extend(check_asset(asset, cfg, root, bans, queue_ids))

    if fails:
        print(f"GATE FAILED, {len(fails)} problems across {len(assets)} assets:\n")
        for fail in fails:
            print(f"  {fail}")
        return 1

    print(f"gate passed: {len(assets)} assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
