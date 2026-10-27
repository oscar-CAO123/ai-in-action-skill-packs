# 27 October 2026

Security for operators: keys, connectors, installs and the agents that run them.

| | On the call | Where |
|---|---|---|
| 1 | Check a skill or repo before you install it | [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) |

## The one tool

Tonight's giveaway lives in NVIDIA's own repository, so you get it from the source. SkillSpector scans
an agent skill, plugin or repo for prompt injection, data theft, hidden commands and risky code, and
gives it a score before anything touches your machine.

Install it by following its README, pinned to the commit we checked:
[`7805bb9`](https://github.com/NVIDIA/skillspector/commit/7805bb94843d91cb9937f57264ca52642164499b).

Then clone what you want to install into a throwaway folder, and before you run anything from it:

```
skillspector scan <folder> --no-llm
```

Read the score, open anything it flags, and only then install. A clean scan covers the version you
scanned. Scan again before every update.
