"""Adapter registry.

Adding a provider means writing a class that implements the contract in base.py and adding a
line here. Nothing above this module knows which vendor is in use.
"""

from __future__ import annotations

from .base import Adapter, ApprovalRequired, CapExceeded, Request, Result, spent_this_week
from .elevenlabs_provider import ElevenLabsAdapter
from .fal_provider import FalAdapter
from .google_provider import GoogleAdapter
from .openai_provider import OpenAIAdapter
from .replicate_provider import ReplicateAdapter

REGISTRY = {
    "openai": OpenAIAdapter,
    "google": GoogleAdapter,
    "replicate": ReplicateAdapter,
    "fal": FalAdapter,
    "elevenlabs": ElevenLabsAdapter,
}


def get(cfg: dict, kind: str) -> Adapter | None:
    """Return the adapter configured for this kind of generation, or None if there is not one."""
    name = (cfg.get("providers") or {}).get(kind)
    if not name:
        return None
    if name not in REGISTRY:
        raise ValueError(f"unknown provider '{name}'. known: {', '.join(sorted(REGISTRY))}")
    settings = (cfg.get("provider_settings") or {}).get(name, {})
    adapter = REGISTRY[name](cfg, settings)
    if kind not in adapter.kinds:
        raise ValueError(f"provider '{name}' does not do {kind}")
    return adapter


__all__ = ["Adapter", "Request", "Result", "ApprovalRequired", "CapExceeded",
           "spent_this_week", "get", "REGISTRY"]
