---
name: build-deterministic-macro
description: Build a bounded desktop or browser macro for a stable, repeated click and keyboard path that needs no model reasoning, with explicit preconditions, dry-run, fail-closed checkpoints, and result verification. Use when you need a macro, fixed click path, keyboard automation, or cheaper deterministic replacement for computer use. Do NOT use for changing layouts, ambiguous targets, personal-data decisions, CAPTCHA, destructive actions, or workflows better served by an API or headless CLI.
---

# Build a deterministic macro

Automate one stable path with no model in the execution loop.

## Gate

Build a macro only when the same starting state can be established every run, each action has a stable accessibility target or anchor, no step requires judgement, the final state is deterministic, and failure can stop before an unsafe action.

Prefer accessibility targets and keyboard shortcuts, then window-relative anchors. Use screen coordinates only when display size, scaling, window position, and app version are fixed and validated at startup.

## Record the path

Capture application and version, window state, display scale, starting screen, ordered actions, expected state after each action, allowed inputs, forbidden data, final verification signal, and recovery action. Separate constants from run inputs. Never record credentials.

## Build

1. Validate app, window, scale, starting state, and input.
2. Add `--dry-run` that prints the resolved path and checks anchors without the final action.
3. Execute one action at a time.
4. Check expected state after every action. Stop on the first mismatch.
5. Put external writes behind an explicit approval flag.
6. Verify the final state independently.
7. Log timestamps, actions, checkpoints, result, and recovery state without sensitive values.

Wait for a named state with a ceiling instead of hiding uncertainty behind long sleeps. Never retry the final action automatically.

## Test

Test the correct state, wrong window or scale, missing control, slow transition, duplicate run, dry-run withholding the final action, and failed final verification.

Done means the happy path passes, every mismatch fails closed before the next action, dry-run makes no external write, and a second run cannot duplicate the outcome.

Read `references/automation-routing.md` when a CLI or computer-use agent may be a better fit.
