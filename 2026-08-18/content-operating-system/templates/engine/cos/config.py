"""Config loading and validation.

Config never holds a secret. It holds the NAME of an environment variable, and the value is
read from the environment at run time. `python3 -m cos.config --check` validates everything
and exits non-zero with the reason if anything is wrong.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

DEFAULTS = {
    "project": {"name": "", "root": ".", "timezone": ""},
    "sources": [],
    "channels": [],
    "formats": [],
    "providers": {"llm": "agent_cli", "image": None, "video": None, "voice": None},
    "ideation": {
        "ideas_per_run": 15,
        "written_up": 5,
        "lookback_days": 7,
        "weights": {
            "independent_sources": 3.0,
            "recency": 2.0,
            "money_behind_it": 2.0,
            "repetition": 1.5,
            "unanswered": 1.0,
        },
    },
    "caps": {"weekly_generation_spend": 0, "per_asset_spend": 0},
    "approval": {
        "ingest": "unattended",
        "ideate": "unattended",
        "paid_generation": "human",
        "publish": "human",
        "system_of_record_write": "human",
    },
    "redaction": {"enabled": True, "keep": ["role", "industry", "size_band", "stage"]},
}


def project_root() -> Path:
    """Resolve the project root from this file, never from the working directory.

    A scheduler starts a job in a directory nobody chose, so cwd is not trustworthy.
    """
    return Path(__file__).resolve().parent.parent.parent


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load(path: Path | None = None) -> dict:
    path = path or (project_root() / "engine" / "config.json")
    if not path.exists():
        raise SystemExit(f"no config at {path}. copy config.example.json and fill it in.")
    with path.open() as handle:
        cfg = _deep_merge(DEFAULTS, json.load(handle))
    cfg["_root"] = str(project_root())
    cfg["_config_path"] = str(path)
    return cfg


def load_dotenv(root: Path | None = None) -> None:
    """Read .env from the project root into os.environ without overwriting what is already set."""
    root = root or project_root()
    env_file = root / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)


def enabled_sources(cfg: dict) -> list[dict]:
    sources = [s for s in cfg.get("sources", []) if s.get("enabled", True)]
    return sorted(sources, key=lambda s: s.get("rank", 99))


def check(cfg: dict) -> list[str]:
    """Return a list of problems. Empty list means the config is usable."""
    problems: list[str] = []
    root = Path(cfg["_root"])

    if not cfg["project"].get("name"):
        problems.append("project.name is empty")

    if not cfg.get("sources"):
        problems.append("no sources configured, so ingestion has nothing to do")

    seen_ids: set[str] = set()
    for source in cfg.get("sources", []):
        sid = source.get("id")
        if not sid:
            problems.append("a source has no id")
            continue
        if sid in seen_ids:
            problems.append(f"duplicate source id: {sid}")
        seen_ids.add(sid)

        if not source.get("type"):
            problems.append(f"{sid}: no type")

        for raw_path in source.get("paths", []):
            expanded = Path(os.path.expanduser(raw_path))
            if not expanded.exists():
                problems.append(f"{sid}: path does not exist: {expanded}")

        token_env = source.get("token_env")
        if token_env and not os.environ.get(token_env):
            problems.append(f"{sid}: ${token_env} is not set in the environment")

    for fmt in cfg.get("formats", []):
        spec = root / "brain" / "formats" / f"{fmt}.md"
        if not spec.exists():
            problems.append(f"format '{fmt}' is selected but {spec} does not exist")

    if cfg["approval"].get("paid_generation") != "human":
        problems.append("approval.paid_generation must be 'human'")
    if cfg["approval"].get("publish") != "human":
        problems.append("approval.publish must be 'human'")

    return problems


def main() -> int:
    load_dotenv()
    cfg = load()
    problems = check(cfg)
    if problems:
        print("config check failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"config ok: {len(enabled_sources(cfg))} enabled sources, "
          f"{len(cfg.get('formats', []))} formats")
    return 0


if __name__ == "__main__":
    sys.exit(main())
