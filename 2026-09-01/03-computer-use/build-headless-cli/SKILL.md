---
name: build-headless-cli
description: Build a tested command-line wrapper for a repeatable application workflow using stable APIs, endpoints, DOM selectors, or local files, with dry-run, explicit inputs, machine-readable output, and fail-closed verification. Use when you need a custom CLI, headless tool, terminal wrapper, or faster repeatable alternative to browser use. Do NOT use when the workflow requires visual judgement, unstable coordinates, CAPTCHA, manual approval inside the UI, or an available supported API already solves the job.
---

# Build a headless CLI

Turn one named application workflow into a deterministic command. Keep browser or computer use for parts that require vision or judgement.

## Route first

Choose the first reliable layer: supported API or existing CLI, custom headless CLI using stable local files, endpoints, or selectors, deterministic macro for a fixed path, then browser or computer use for vision or changing layouts. Stop if a supported API already covers the workflow unless the wrapper adds a stable business contract, validation, or output format.

## Define the command contract

Resolve one job, exact inputs, exact output, definition of done, authentication source, read or write mode, duplicate-prevention rule, rate and cost ceilings, exit codes, JSON schema, and human gate before external writes.

Default interface: `tool <verb> [required inputs] [--dry-run] [--json]`.

Exit `0` on verified success, `2` on invalid input, `3` on blocked authentication or permission, `4` on remote or UI drift, and `5` on an unverified write.

## Build

1. Inspect supported interfaces and current local tooling.
2. Record one successful manual trace and identify stable boundaries.
3. Implement the smallest command around those boundaries.
4. Validate inputs before opening a session or making a request.
5. Make `--dry-run` exercise every step except the final write.
6. Emit JSON with requested action, resolved targets, changes, skips, evidence, and status.
7. Verify the result from a fresh read. Never infer success from a request or click alone.
8. Add fixture tests for happy path, missing input, duplicate run, authentication failure, drift, partial failure, and limit reached.

Prefer semantic selectors, accessible names, and stable attributes. Never encode screen coordinates in a headless CLI. Save sessions only in the approved credential or browser-profile location.

## Failure rules

Stop on CAPTCHA, login challenge, changed destination, missing selector, ambiguous match, or unexpected write scope. Never retry a write blindly. A partial batch records each confirmed item and leaves unconfirmed items retryable. Re-running the same command must not duplicate confirmed work.

## Deliver

Provide the executable, concise `--help`, fixtures, tests, and one commands file. Done means dry-run is accurate, tests pass, success verifies from a fresh read, duplicate execution is safe, and failure exits are demonstrated.

Read `references/automation-routing.md` when the correct layer is unclear.
