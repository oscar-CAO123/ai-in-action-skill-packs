"""Production, one approved idea at a time.

Not scheduled, deliberately. Production is where the money and the publishing risk sit, so it
stays attached to a person. Every step stops and waits.

    python3 -m cos.produce --queue 2026-09-01 --idea 3 --step script
    python3 -m cos.produce --queue 2026-09-01 --idea 3 --step stills   # needs an approved batch
    python3 -m cos.produce --queue 2026-09-01 --idea 3 --step render
    python3 -m cos.gate outputs/drafts/2026-09-01-i3/batch.json

The order is the whole point, because every gate sits before the spend it protects:

    script  ->  HUMAN  ->  stills  ->  HUMAN  ->  motion and voice  ->  gate  ->  HUMAN  ->  publish
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import config as config_module
from .adapters import ApprovalRequired, CapExceeded, Request, get, spent_this_week
from .agent import ask

STEPS = ("script", "stills", "render")


def load_idea(root: Path, queue_date: str, rank: int) -> dict:
    path = root / "outputs" / "queue" / queue_date / "queue.json"
    if not path.exists():
        raise SystemExit(f"no queue at {path}")
    queue = json.loads(path.read_text())
    for idea in queue.get("ideas", []):
        if int(idea.get("rank", 0)) == rank:
            return idea
    raise SystemExit(f"no idea at rank {rank} in {path}")


def draft_dir(root: Path, queue_date: str, rank: int) -> Path:
    path = root / "outputs" / "drafts" / f"{queue_date}-i{rank}"
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------- script

def step_script(cfg: dict, idea: dict, out: Path) -> int:
    root = Path(cfg["_root"])
    fmt = idea.get("format") or (cfg.get("formats") or [""])[0]
    spec = root / "brain" / "formats" / f"{fmt}.md"

    evidence = "\n".join(
        f"- {e['source_type']} {e['date']} ({e['record_id']}): {e['text']}"
        for e in idea.get("evidence_detail", [])
    )

    prompt = f"""Write the full script for one asset.

Read `brain/SKILL.md`, `brain/copywriting.md`, `brain/language-rules.md`, and
`{spec.relative_to(root) if spec.exists() else 'brain/formats/'}`.

Hook: {idea.get('hook', '')}
Hook structure: {idea.get('hook_structure', '')}
Angle: {idea.get('angle', '')}
Format: {fmt}
Proof tier: {idea.get('proof_tier', '')}
Founder question: {idea.get('founder_question', '')}

The evidence this asset is built on:
{evidence}

Write the script to the format's beats. Every claim stays inside the proof tier above.
No em dashes. No "it is not X, it is Y". No banned words.

Return ONLY the script text, ready to be read aloud or posted. No preamble, no commentary.
"""
    output, detail = ask(prompt, cwd=root)
    if output is None:
        print(f"script step needs an agent: {detail}")
        print("write the script by hand to", out / "script.md")
        return 1

    (out / "script.md").write_text(output.strip() + "\n")
    (out / "idea.json").write_text(json.dumps(idea, indent=2, ensure_ascii=False))
    print(f"script written to {out / 'script.md'} via {detail}")
    print("\nHUMAN GATE. Read it, edit it, and only then run --step stills.")
    return 0


# ---------------------------------------------------------------------- stills

def step_stills(cfg: dict, idea: dict, out: Path, count: int) -> int:
    adapter = get(cfg, "image")
    if adapter is None:
        print("no image provider configured. This format may not need one.")
        return 0

    script_path = out / "script.md"
    if not script_path.exists():
        print("no script.md. Run --step script first and approve it.")
        return 1

    prompts_path = out / "prompts.json"
    if not prompts_path.exists():
        print(f"no prompts.json. Write {count} image prompts to it, one per beat, then re-run.")
        print('  format: [{"beat": 1, "prompt": "..."}]')
        return 1

    prompts = json.loads(prompts_path.read_text())[:count]
    root = Path(cfg["_root"])
    print(f"spent this week: ${spent_this_week(root):.2f} of "
          f"${cfg['caps'].get('weekly_generation_spend', 0):.2f}")

    made = 0
    for entry in prompts:
        target = out / "stills" / f"beat-{entry['beat']:02d}.png"
        if target.exists():
            print(f"  beat {entry['beat']}: exists, skipping")
            continue
        request = Request(kind="image", prompt=entry["prompt"], out_path=target,
                          aspect=entry.get("aspect", "9:16"))
        try:
            result = adapter.generate(request)
        except (ApprovalRequired, CapExceeded) as error:
            print(f"\nSTOPPED: {error}")
            return 1
        if result.ok:
            print(f"  beat {entry['beat']}: {target} (${result.cost_usd:.2f})")
            made += 1
        else:
            print(f"  beat {entry['beat']}: failed, {result.detail}")

    print(f"\n{made} stills. HUMAN GATE. Look at every one before --step render.")
    print("A bad still becomes a bad video every single time.")
    return 0


# ---------------------------------------------------------------------- render

def step_render(cfg: dict, idea: dict, out: Path) -> int:
    root = Path(cfg["_root"])
    stills = sorted((out / "stills").glob("*.png"))
    if not stills:
        print("no approved stills. Run --step stills first.")
        return 1

    voice_adapter = get(cfg, "voice")
    if voice_adapter and (out / "script.md").exists():
        vo_path = out / "voice.mp3"
        if not vo_path.exists():
            text = (out / "script.md").read_text()
            try:
                result = voice_adapter.generate(
                    Request(kind="voice", prompt=text, out_path=vo_path))
            except (ApprovalRequired, CapExceeded) as error:
                print(f"STOPPED: {error}")
                return 1
            print(f"  voice: {vo_path} (${result.cost_usd:.2f})"
                  if result.ok else f"  voice failed: {result.detail}")

    video_adapter = get(cfg, "video")
    if video_adapter:
        motion_path = out / "prompts-motion.json"
        if motion_path.exists():
            for entry in json.loads(motion_path.read_text()):
                target = out / "clips" / f"beat-{entry['beat']:02d}.mp4"
                if target.exists():
                    continue
                try:
                    result = video_adapter.generate(Request(
                        kind="video", prompt=entry["prompt"], out_path=target,
                        duration=entry.get("duration", 5), aspect=entry.get("aspect", "9:16")))
                except (ApprovalRequired, CapExceeded) as error:
                    print(f"STOPPED: {error}")
                    return 1
                print(f"  beat {entry['beat']}: {target} (${result.cost_usd:.2f})"
                      if result.ok else f"  beat {entry['beat']} failed: {result.detail}")

    batch = {
        "assets": [{
            "id": out.name,
            "idea_id": str(idea.get("id") or idea.get("rank")),
            "format": idea.get("format", ""),
            "hook": idea.get("hook", ""),
            "hook_structure": idea.get("hook_structure", ""),
            "script": (out / "script.md").read_text() if (out / "script.md").exists() else "",
            "proof_tier": idea.get("proof_tier", ""),
            "evidence": [e["record_id"] for e in idea.get("evidence_detail", [])],
            "framed_as_position": idea.get("proof_tier") == "held",
        }]
    }
    batch_path = out / "batch.json"
    batch_path.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
    print(f"\nbatch written: {batch_path}")
    print(f"now run: python3 -m cos.gate {batch_path.relative_to(root)}")
    print("The gate must exit 0 before this is finished. Publishing is a person's job.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="produce one approved idea")
    parser.add_argument("--queue", required=True, help="queue date, e.g. 2026-09-01")
    parser.add_argument("--idea", required=True, type=int, help="rank in that queue")
    parser.add_argument("--step", required=True, choices=STEPS)
    parser.add_argument("--count", type=int, default=8, help="stills to make")
    args = parser.parse_args()

    config_module.load_dotenv()
    cfg = config_module.load()
    root = Path(cfg["_root"])
    idea = load_idea(root, args.queue, args.idea)
    out = draft_dir(root, args.queue, args.idea)

    if args.step == "script":
        return step_script(cfg, idea, out)
    if args.step == "stills":
        return step_stills(cfg, idea, out, args.count)
    return step_render(cfg, idea, out)


if __name__ == "__main__":
    sys.exit(main())
