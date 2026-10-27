"""The provider adapter contract.

One neutral interface for image, video and voice. Adapters translate it to a vendor. Nothing
above this module knows which vendor is in use, so swapping one is a config change.

Two things are enforced here rather than in each adapter, because a guard that lives in the
code you remembered to write is not a guard:

1. Every paid call passes through `spend_guard`, which refuses without an explicit approval
   token and refuses again if the weekly cap would be exceeded.
2. Every call is logged to outputs/logs/spend.jsonl before the request is made, so a run that
   dies halfway still leaves a record of what it was about to spend.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path


class ApprovalRequired(RuntimeError):
    """Raised when a paid call is attempted without an approval token."""


class CapExceeded(RuntimeError):
    """Raised when a paid call would take the week past the configured cap."""


@dataclass
class Request:
    kind: str                      # "image" | "video" | "voice"
    prompt: str
    out_path: Path
    references: list[Path] = field(default_factory=list)
    duration: float | None = None  # video and voice, seconds
    aspect: str | None = None      # "9:16", "1:1", "16:9"
    voice_id: str | None = None
    extra: dict = field(default_factory=dict)


@dataclass
class Result:
    ok: bool
    path: Path | None
    cost_usd: float
    provider: str
    detail: str = ""


APPROVAL_ENV = "COS_APPROVED_BATCH"


def spend_guard(cfg: dict, estimated: float, note: str) -> None:
    """The single choke point above every paid call. Never call a provider without it."""
    if cfg["approval"].get("paid_generation") != "human":
        raise ApprovalRequired(
            "approval.paid_generation must be 'human'. This system does not spend on a schedule."
        )

    token = os.environ.get(APPROVAL_ENV)
    if not token:
        raise ApprovalRequired(
            f"paid generation needs an approved batch. Set {APPROVAL_ENV} to the batch id the "
            f"operator approved. Refusing: {note} (est ${estimated:.2f})"
        )

    root = Path(cfg["_root"])
    cap = float(cfg["caps"].get("weekly_generation_spend") or 0)
    per_asset = float(cfg["caps"].get("per_asset_spend") or 0)

    if per_asset and estimated > per_asset:
        raise CapExceeded(
            f"${estimated:.2f} exceeds the per-asset cap of ${per_asset:.2f}: {note}"
        )

    if cap:
        spent = spent_this_week(root)
        if spent + estimated > cap:
            raise CapExceeded(
                f"${estimated:.2f} would take the week to ${spent + estimated:.2f}, "
                f"past the ${cap:.2f} cap. Nothing was spent."
            )


def spent_this_week(root: Path) -> float:
    ledger = root / "outputs" / "logs" / "spend.jsonl"
    if not ledger.exists():
        return 0.0
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec="seconds")
    total = 0.0
    for line in ledger.read_text().splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("at", "") >= cutoff:
            total += float(entry.get("cost_usd") or 0)
    return total


def log_spend(root: Path, provider: str, kind: str, cost: float, note: str) -> None:
    ledger = root / "outputs" / "logs" / "spend.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as handle:
        handle.write(json.dumps({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "provider": provider,
            "kind": kind,
            "cost_usd": round(cost, 4),
            "batch": os.environ.get(APPROVAL_ENV, ""),
            "note": note[:200],
        }) + "\n")


class Adapter:
    name = "unset"
    kinds: tuple[str, ...] = ()

    def __init__(self, cfg: dict, settings: dict | None = None):
        self.cfg = cfg
        self.settings = settings or {}
        self.root = Path(cfg["_root"])

    def token(self) -> str | None:
        name = self.settings.get("token_env")
        return os.environ.get(name) if name else None

    def estimate(self, request: Request) -> float:
        """Estimated cost in USD, before the call. Adapters override with their rate card."""
        return 0.0

    def generate(self, request: Request) -> Result:
        """Run the generation. Must call `spend_guard` and `log_spend`, in that order."""
        raise NotImplementedError

    # ---------------------------------------------------------------- shared path

    def _guarded(self, request: Request, run) -> Result:
        estimated = self.estimate(request)
        note = f"{self.name} {request.kind}: {request.prompt[:80]}"
        spend_guard(self.cfg, estimated, note)
        log_spend(self.root, self.name, request.kind, estimated, note)
        try:
            path = run()
        except Exception as error:
            return Result(False, None, estimated, self.name, f"{type(error).__name__}: {error}")
        return Result(True, path, estimated, self.name)
