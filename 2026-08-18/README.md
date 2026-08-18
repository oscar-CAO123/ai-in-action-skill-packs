# 18 August 2026

Three skills, given away on the AI in Action call, Tuesday 18 August 2026. They are one system: a
diary that captures what you know, a trigger that reads it and picks the work, and a gauntlet that
builds the work to a bar.

Root of the repo: [../README.md](../README.md). Licence: MIT, see [../LICENSE](../LICENSE).

Every one of these is a **skill file**: plain markdown your coding agent reads before it does the
work. Claude Code, Codex, OpenClaw, Hermes, whatever you run. Nothing to install, no account, no
service in the middle. Point your agent at a folder and tell it to follow the file.

## The idea behind the drop

Allie K. Miller runs 34 agents. On Greg Isenberg's podcast on 18 August 2026 she said her strongest
prompt is three words: **do smart things**. It works because it sits on top of every context document
she owns, and because she stopped managing the agents and started enabling them.

Two things have to be true for three words to work. The agent has to be able to read your world, and
it has to have a bar to build against. That is what the three skills are.

## The packs

### `diary/`
The context that never lands in a meeting, an email or a commit. Three short prompts, dictated, filed
dated, then extracted into an index of decisions, corrections, people and open loops. The corrections
section is the valuable one: every line is a wrong belief someone was about to repeat.

Run it at the end of a day. It takes about five minutes.

### `do-smart-things/`
The three words. It sweeps your tree indexes first, reads the diary index above everything else,
caches a context map so later runs start instantly, then names the single highest-value thing to
build next and tells you why it beat the runners-up. You say yes. It builds it through the gauntlet,
then writes back to the diary so the next run knows what happened.

It stops at a human gate before any push, deploy, send, post, paid call or production write. Every
time, without exception, including when the task would obviously be better if it did not.

### `gauntlet-goal/`
The bar. One maker writes, one critic grades, and the critic never sees who wrote it or how many
tries it took. Pieces get owners, criteria get answer keys written before any maker starts, and
nothing integrates until it passes. `do-smart-things` builds through this.

Useful on its own for taking a working first version to showcase quality.

## Running them

```
1. Copy the folder you want into your own project, or clone the repo.
2. Open your agent in that folder.
3. Tell it: read <skill file> and follow it.
```

Start with `diary/` and run it for a week before you try the three words. `do-smart-things` on an
empty tree gives you a guess. On a tree with a fortnight of diary entries it gives you the thing you
were about to ask for.

## What this supersedes

Nothing. The 11 August packs stand as they shipped.
