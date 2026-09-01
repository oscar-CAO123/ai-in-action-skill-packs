"""Google Gemini images and video."""

from __future__ import annotations

import base64
import time
from pathlib import Path

import requests

from .base import Adapter, Request, Result

BASE = "https://generativelanguage.googleapis.com/v1beta"


class GoogleAdapter(Adapter):
    name = "google"
    kinds = ("image", "video")

    def estimate(self, request: Request) -> float:
        if request.kind == "video":
            return float(self.settings.get("video_rate_per_second", 0.35)) * (request.duration or 8)
        return float(self.settings.get("image_rate", 0.04))

    def generate(self, request: Request) -> Result:
        if request.kind == "image":
            return self._guarded(request, lambda: self._image(request))
        return self._guarded(request, lambda: self._video(request))

    def _image(self, request: Request) -> Path:
        model = self.settings.get("image_model", "imagen-4.0-generate-001")
        response = requests.post(
            f"{BASE}/models/{model}:predict?key={self.token()}",
            json={
                "instances": [{"prompt": request.prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": request.aspect or "1:1"},
            },
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()["predictions"][0]["bytesBase64Encoded"]
        request.out_path.parent.mkdir(parents=True, exist_ok=True)
        request.out_path.write_bytes(base64.b64decode(data))
        return request.out_path

    def _video(self, request: Request) -> Path:
        model = self.settings.get("video_model", "veo-3.0-generate-001")
        start = requests.post(
            f"{BASE}/models/{model}:predictLongRunning?key={self.token()}",
            json={"instances": [{"prompt": request.prompt}],
                  "parameters": {"aspectRatio": request.aspect or "9:16"}},
            timeout=120,
        )
        start.raise_for_status()
        operation = start.json()["name"]

        for _ in range(120):
            time.sleep(10)
            poll = requests.get(f"{BASE}/{operation}?key={self.token()}", timeout=60)
            poll.raise_for_status()
            body = poll.json()
            if body.get("done"):
                uri = body["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                request.out_path.parent.mkdir(parents=True, exist_ok=True)
                request.out_path.write_bytes(
                    requests.get(f"{uri}&key={self.token()}", timeout=600).content)
                return request.out_path
        raise TimeoutError("video generation did not finish in 20 minutes")
