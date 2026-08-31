"""OpenAI images."""

from __future__ import annotations

import base64
from pathlib import Path

import requests

from .base import Adapter, Request, Result

RATES = {"low": 0.02, "medium": 0.07, "high": 0.19}


class OpenAIAdapter(Adapter):
    name = "openai"
    kinds = ("image",)

    def estimate(self, request: Request) -> float:
        return RATES.get(self.settings.get("quality", "medium"), 0.07)

    def generate(self, request: Request) -> Result:
        def run() -> Path:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {self.token()}"},
                json={
                    "model": self.settings.get("model", "gpt-image-1"),
                    "prompt": request.prompt,
                    "size": _size(request.aspect),
                    "quality": self.settings.get("quality", "medium"),
                    "n": 1,
                },
                timeout=300,
            )
            response.raise_for_status()
            payload = response.json()["data"][0]
            request.out_path.parent.mkdir(parents=True, exist_ok=True)
            if payload.get("b64_json"):
                request.out_path.write_bytes(base64.b64decode(payload["b64_json"]))
            else:
                request.out_path.write_bytes(requests.get(payload["url"], timeout=120).content)
            return request.out_path

        return self._guarded(request, run)


def _size(aspect: str | None) -> str:
    return {"9:16": "1024x1536", "16:9": "1536x1024"}.get(aspect or "1:1", "1024x1024")
