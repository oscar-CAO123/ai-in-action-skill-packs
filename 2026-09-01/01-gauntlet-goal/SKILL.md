---
name: gauntlet-goal
description: Build a bounded maker and critic loop that takes a strong first version, or a fog-cleared specification, to showcase quality through parallel specialist work and blind verification. Use when the user says "gauntlet goal", types "$gauntlet-goal", asks to polish an MVP with subagents, wants makers paired with independent critics, or needs a showcase build from concrete references or a binary answer key. Do NOT use for one-shot tasks, vague first drafts, unsettled product direction, or work whose parts cannot be verified independently.
---

# Gauntlet goal

One maker writes, one critic grades, and the critic never sees who wrote it. That is the whole idea.
Everything else here exists to make that comparison honest.

Produce one self-contained prompt the user can run, saved to a file. Do not start the run yourself
unless the user asks for it inline.

## Gate

All four must hold before you build the loop:

1. A working first version, a close reference, or a fog-cleared decision map plus an answer key.
2. The work separates into independent pieces with explicit ownership.
3. Each piece has a reference or a measurable acceptance bar.
4. The expected gain justifies several agents, more tokens and a longer run.

A gauntlet intensifies whatever direction it receives, so an unresolved decision wastes more effort
faster than it would in a single-agent run. Send ordinary self-verifying work to a simple loop.

## Clear the fog

Pick one source of truth:

- **Reference branch.** An existing product, a strong first version, or a concrete artifact critics
  can compare against blind.
- **Novel-work branch.** Build a decision map and an answer key before writing the prompt.

For novel work, list every undecided question. Mark one `ready` when its dependencies are settled and
`fog` when evidence or a prior decision is missing. Clear each fog item with targeted research, a
rough prototype the user reacts to, or a real check against the world. Never let an agent fill fog
with an assumption.

The decision map records each question, its dependencies, the answer, the evidence, the reason, and
what it unlocks. The answer key converts the settled map into atomic pass or fail checks, each naming
its artifact, its verification method and the expected result. The user approves both before makers
begin.

## Interview

Use what the user already told you. Ask only for what is missing:

- The baseline or reference paths. For novel work, the decision map and answer key paths.
- The outcome for version two, in one sentence.
- The independent pieces that can be built and checked separately.
- The acceptance bar for each piece, and for the assembled whole.
- The files and systems each worker may touch.
- The ceilings: agents, repair passes, wall time, spend.
- Where the final artifact, the evidence and the pass log go.

If the user cannot name a checkable bar, stop and build the answer key first.

## Build the graph

Use the smallest graph that raises quality:

1. **Planner.** Inspects the baseline, splits the work into the smallest independent pieces, declares
   dependencies, and assigns exactly one writer per file.
2. **Maker per piece.** Improves only its owned piece, against the supplied reference and rubric.
3. **Blind critic per piece.** Sees the artifact, the evidence and the answer key. Never the maker's
   commentary and never the iteration count. Returns pass or fail, scores by criterion, and concrete
   defects. A critic evaluates and never repairs.
4. **Repair loop.** Failed criteria go back to the same maker. The critic re-runs after the artifact
   changes.
5. **Integrator.** Assembles passed pieces only and resolves interfaces without redesigning them.
6. **Whole-product critic.** Tests the assembled result against the brief, the references and every
   objective check.
7. **Human gate.** Stop before any external write, publish, send, deploy, paid action or irreversible
   change.

Parallelise only pieces with no shared write target. Serialise dependencies. One file has one writer
at a time.

## Set the bar

Translate "make it good" into evidence:

- Every criterion gets a binary check or a numeric rubric, written before makers begin.
- Require exact commands, screenshots, source comparisons or test output.
- Use a separate critic for anything judged by eye.
- Keep failures in the pass log. A critic's prose counts as evidence only when it names the artifact
  and the criterion it checked.
- Stop when every local critic passes and the whole-product critic passes.

## Hard stop

Every prompt sets a maximum number of active agents, repair passes per piece, a total time or spend
ceiling, and an escape after two consecutive passes with no measurable improvement. Stop immediately
on conflicting writes, a missing reference, a permission boundary, or a baseline that needs redesign
rather than repair.

## Prompt contract

Write one self-contained prompt with these sections:

```text
GOAL
BASELINE, REFERENCES, OR APPROVED DECISION MAP
ANSWER KEY
PIECES, DEPENDENCIES, AND FILE OWNERSHIP
ACCEPTANCE BAR PER PIECE
WHOLE-PRODUCT BAR
GRAPH: planner, makers, blind critics, integrator, final critic
VERIFICATION COMMANDS AND EVIDENCE
HARD STOP
HUMAN GATES
ON STOP, RETURN
DO NOT
```

Require a pass log carrying agent, owned piece, artifact path, critic result, changed criteria and
next action. Require the final response to name the artifacts, the evidence paths, the final scores,
the remaining failures, and every external write attempted.

## Check your own prompt before handing it over

The baseline or approved decision map is named by path. The answer key predates execution. Every
piece has one writer and one blind critic. Critics cannot edit. Dependencies prevent conflicting
edits. Every criterion has a verification action. Failed pieces cannot integrate. The assembled
result gets a final check. Every ceiling exists. External writes stop at a human gate. No em dashes.
