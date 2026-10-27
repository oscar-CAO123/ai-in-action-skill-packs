"""Replicate: whatever model the operator names, image or video."""

from __future__ import annotations

import time
from pathlib import Path

import requests

from .base import Adapter, Request, Result


class ReplicateAdapter(Adapter):
    name = "replicate"
    kinds = ("image", "video")

    def estimate(self, request: Request) -> float:
        key = "video_rate" if request.kind == "video" else "image_rate"
        return float(self.settings.get(key, 0.05 if request.kind == "image" else 0.50))

    def generate(self, request: Request) -> Result:
        def run() -> Path:
            model = self.settings[f"{request.kind}_model"]
            payload = {"input": {"prompt": request.prompt}}
            if request.aspect:
                payload["input"]["aspect_ratio"] = request.aspect
            if request.duration:
                payload["input"]["duration"] = request.duration

            start = requests.post(
                f"https://api.replicate.com/v1/models/{model}/predictions",
                headers={"Authorization": f"Bearer {self.token()}",
                         "Prefer": "wait"},
                json=payload,
                timeout=600,
            )
            start.raise_for_status()
            body = start.json()

            while body.get("status") in ("starting", "processing"):
                time.sleep(5)
                body = requests.get(body["urls"]["get"],
                                    headers={"Authorization": f"Bearer {self.token()}"},
                                    timeout=60).json()

            if body.get("status") != "succeeded":
                raise RuntimeError(f"replicate {body.get('status')}: {body.get('error')}")

            output = body["output"]
            url = output[0] if isinstance(output, list) else output
            request.out_path.parent.mkdir(parents=True, exist_ok=True)
            request.out_path.write_bytes(requests.get(url, timeout=600).content)
            return request.out_path

        return self._guarded(request, run)
