"""Source registry.

Adding a source type means writing a class that implements the contract in base.py and
registering it here. Nothing above this module needs to know it exists.
"""

from .base import Source
from .calls import CallsSource
from .forums import ForumsSource
from .reviews import ReviewsSource
from .tickets import TicketsSource

REGISTRY = {
    "calls": CallsSource,
    "tickets": TicketsSource,
    "forums": ForumsSource,
    "reviews": ReviewsSource,
}


def build(spec: dict) -> Source:
    source_type = spec.get("type")
    if source_type not in REGISTRY:
        raise ValueError(
            f"unknown source type '{source_type}'. known: {', '.join(sorted(REGISTRY))}"
        )
    return REGISTRY[source_type](spec)
