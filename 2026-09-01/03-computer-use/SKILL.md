---
name: computer-use
description: The router for letting an agent operate software on your behalf. Covers driving a real screen, wrapping a stable workflow in a command line, recording a fixed click path as a macro, and one worked end-to-end example in LinkedIn outreach. Use when you want an agent to do something in an application, or when you are deciding between computer use, a CLI and a macro. Do NOT use for work an official API already solves cleanly.
---

# Computer use

Four skills, and the order below is the order to try them in. Every one of them is slower, more
expensive and more fragile than the one after it, so read this page before you pick.

## Pick the cheapest thing that works

1. **An official API.** If one exists and covers the job, stop. None of these skills apply.
2. **`build-headless-cli`.** The workflow runs on stable endpoints, DOM selectors or local files.
   Wrap it in one deterministic command with a dry run, explicit inputs and machine-readable output.
   Fastest and cheapest to run, and it does not care what the screen looks like.
3. **`build-deterministic-macro`.** The path is a stable, repeated sequence of clicks and keys that
   needs no judgement. Bound it with preconditions, a dry run, fail-closed checkpoints and a result
   check.
4. **`codex-computer-use`.** The layout moves, the target is ambiguous, or the job needs the agent to
   look at the screen and decide. This is the expensive one. It is also the only one that handles a
   page it has never seen.

`references/automation-routing.md`, inside both `build-headless-cli` and
`build-deterministic-macro`, is the long version of this decision.

## The worked example

`linkedin-outreach` is all three ideas in one job: an approved batch of connection invitations sent
through supervised computer use, with recipient verification, a canonical template, mapped profile
variants and a durable contacted ledger.

Read it even if you never send a LinkedIn invitation. It is the shape every safe agent action takes:
**the agent proposes, a human approves the specific action, and a separate record proves what
happened.** Never give an agent a credential and a send button in the same step.

## The rule that keeps this safe

An agent driving your screen can do anything you can do. Every skill in here fails closed: it stops
and asks rather than guessing, it verifies the result rather than assuming the click landed, and it
treats sending, posting, paying and deleting as actions that need a fresh yes each time.
