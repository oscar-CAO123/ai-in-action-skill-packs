"""fal.ai: whatever endpoint the operator names."""

from __future__ import annotations

import time
from pathlib import Path

import requests

from .base import Adapter, Request, Result


class FalAdapter(Adapter):
    name = "fal"
    kinds = ("image", "video")

    def estimate(self, request: Request) -> float:
        key = "video_rate" if request.kind == "video" else "image_rate"
        return float(self.settings.get(key, 0.04 if request.kind == "image" else 0.40))

    def generate(self, request: Request) -> Result:
        def run() -> Path:
            endpoint = self.settings[f"{request.kind}_endpoint"]
            headers = {"Authorization": f"Key {self.token()}"}
            payload = {"prompt": request.prompt}
            if request.aspect:
                payload["aspect_ratio"] = request.aspect
            if request.duration:
                payload["duration"] = request.duration

            start = requests.post(f"https://queue.fal.run/{endpoint}",
                                  headers=headers, json=payload, timeout=120)
            start.raise_for_status()
            status_url = start.json()["status_url"]
            response_url = start.json()["response_url"]

            for _ in range(180):
                time.sleep(5)
                status = requests.get(status_url, headers=headers, timeout=60).json()
                if status.get("status") == "COMPLETED":
                    break
                if status.get("status") == "FAILED":
                    raise RuntimeError("fal reported FAILED")
            else:
                raise TimeoutError("fal did not finish in 15 minutes")

            result = requests.get(response_url, headers=headers, timeout=120).json()
            media = result.get("images") or result.get("video") or result.get("output")
            url = media[0]["url"] if isinstance(media, list) else media["url"]
            request.out_path.parent.mkdir(parents=True, exist_ok=True)
            request.out_path.write_bytes(requests.get(url, timeout=600).content)
            return request.out_path

        return self._guarded(request, run)
