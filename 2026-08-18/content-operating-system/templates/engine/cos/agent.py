"""Calling the operator's own agent, headless.

The ideation run needs judgement. Rather than adding an LLM API key and a second bill, it
shells out to whatever agent CLI the operator already pays for. Detection is by trying the
binary, never by assuming a product name means a capability.

If nothing is reachable, ideation degrades to rule-based ranking and says so on the page. It
never quietly produces a worse queue without telling anyone.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

# Each entry: binary, the argv that takes a prompt on the command line, and a probe prompt.
CANDIDATES = [
    ("claude", lambda p: ["claude", "-p", p]),
    ("codex", lambda p: ["codex", "exec", p]),
    ("gemini", lambda p: ["gemini", "-p", p]),
    ("opencode", lambda p: ["opencode", "run", p]),
    ("crush", lambda p: ["crush", "run", "-q", p]),
    ("llm", lambda p: ["llm", p]),
]

PROBE = "Reply with exactly: OK"


def detect(cache_path: Path | None = None) -> tuple[str, callable] | None:
    """Find a working headless agent CLI. Caches the answer, because probing costs a call."""
    if cache_path and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text()).get("agent")
        except json.JSONDecodeError:
            cached = None
        if cached:
            for name, argv in CANDIDATES:
                if name == cached:
                    return name, argv

    for name, argv in CANDIDATES:
        if not shutil.which(name):
            continue
        try:
            result = subprocess.run(argv(PROBE), capture_output=True, text=True, timeout=120)
        except (subprocess.TimeoutExpired, OSError):
            continue
        if result.returncode == 0 and "OK" in result.stdout:
            if cache_path:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(json.dumps({"agent": name}))
            return name, argv
    return None


def ask(prompt: str, cwd: Path, timeout: int = 900,
        cache_path: Path | None = None) -> tuple[str | None, str]:
    """Run one headless call. Returns (output, agent_name) or (None, reason)."""
    found = detect(cache_path)
    if not found:
        return None, "no headless agent CLI found"

    name, argv = found
    env = dict(os.environ)
    try:
        result = subprocess.run(argv(prompt), capture_output=True, text=True,
                                timeout=timeout, cwd=str(cwd), env=env)
    except subprocess.TimeoutExpired:
        return None, f"{name} timed out after {timeout}s"
    except OSError as error:
        return None, f"{name} failed to start: {error}"

    if result.returncode != 0:
        return None, f"{name} exited {result.returncode}: {result.stderr.strip()[:400]}"
    return result.stdout, name


def ask_json(prompt: str, cwd: Path, timeout: int = 900,
             cache_path: Path | None = None) -> tuple[dict | list | None, str]:
    """Same, but pull the first JSON object or array out of the reply.

    Agents narrate. The JSON is in there, usually inside a fenced block, and this finds it
    rather than demanding the agent behave.
    """
    output, detail = ask(prompt, cwd, timeout, cache_path)
    if output is None:
        return None, detail

    text = output.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts[1:]:
            body = part.split("\n", 1)[-1] if part[:20].strip().lower() in ("json", "") else part
            candidate = body.strip().rstrip("`").strip()
            parsed = _try_parse(candidate)
            if parsed is not None:
                return parsed, detail

    for opener, closer in (("[", "]"), ("{", "}")):
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end > start:
            parsed = _try_parse(text[start:end + 1])
            if parsed is not None:
                return parsed, detail

    return None, f"{detail} replied without usable JSON"


def _try_parse(candidate: str):
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None
