"""ElevenLabs voice."""

from __future__ import annotations

from pathlib import Path

import requests

from .base import Adapter, Request, Result


class ElevenLabsAdapter(Adapter):
    name = "elevenlabs"
    kinds = ("voice",)

    def estimate(self, request: Request) -> float:
        # Character-priced. The default here is the rough per-thousand-character rate.
        return len(request.prompt) / 1000 * float(self.settings.get("rate_per_1k_chars", 0.18))

    def generate(self, request: Request) -> Result:
        def run() -> Path:
            voice = request.voice_id or self.settings.get("voice_id")
            if not voice:
                raise ValueError("no voice_id set")
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
                headers={"xi-api-key": self.token(), "Content-Type": "application/json"},
                json={
                    "text": request.prompt,
                    "model_id": self.settings.get("model", "eleven_multilingual_v2"),
                    "voice_settings": self.settings.get(
                        "voice_settings", {"stability": 0.5, "similarity_boost": 0.75}),
                },
                timeout=300,
            )
            response.raise_for_status()
            request.out_path.parent.mkdir(parents=True, exist_ok=True)
            request.out_path.write_bytes(response.content)
            return request.out_path

        return self._guarded(request, run)
