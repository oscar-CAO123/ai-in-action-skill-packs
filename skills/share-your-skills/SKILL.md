---
name: share-your-skills
description: Turn a folder of skills into a GitHub repository that installs as a Claude Code plugin, so a whole team gets them with one command and every later change arrives by itself. Use when the user says "share my skills", "share these with my team", "make this a plugin", "publish my skills", "set up a skills marketplace", or asks how to stop copying skill folders around. Do NOT use to install somebody else's plugin, or to publish anything containing credentials or client data.
---

# Share your skills with your team

Skills in a folder on one laptop help one person. This turns them into a repository that installs as
a plugin, which is the only sharing method that survives a non-technical teammate.

**What you are building.** One GitHub repository that is both a marketplace and the plugin inside
it. Two small JSON files do that. Everyone adds the repository once, installs the plugin once, and
every change you push afterwards lands on their machine on its own.

Drive, Dropbox and Obsidian all fail here for the same reason: the agent reads skills from its own
directory, so somebody has to symlink a synced folder into it, and that breaks the first time a
person who does not think in file paths joins the team.

## Before you start

Confirm all three, and stop and ask if any is missing.

1. **A folder of skills.** Each skill is a directory with a `SKILL.md` inside it. If they have loose
   `.md` files instead, each one becomes its own directory with the file renamed to `SKILL.md`.
2. **GitHub access.** Either the `gh` CLI authenticated (`gh auth status`), or a personal access
   token with `repo` scope in an environment variable. Ask which they have. Never read a token out
   of a file and never print one.
3. **A decision on public or private.** Private repositories work as plugins for anyone whose git
   credentials can read them. Default to private and ask.

## Step 1. Read what they actually have, and say it back

List every skill directory and read the `name` and `description` from each `SKILL.md` frontmatter.
Show them the list and get a yes before touching anything.

Three things to check while you read, because each one causes a real failure later:

- **A `name` in the frontmatter that does not match its directory name.** Normalise it to the
  directory name. Mismatches make skills hard to invoke.
- **Anything private.** Client names, real customer data, internal URLs, and above all credentials.
  Grep for the obvious shapes before a repository exists. Ask about anything you are unsure of, and
  leave it out by default.
- **Deeply nested skills.** Only `skills/<name>/SKILL.md` is discovered. If they have a pack with
  sub-skills underneath it, that is fine, but the top level needs its own `SKILL.md` acting as a
  router, or the sub-skills are invisible.

## Step 2. Lay the repository out

```
<repo>/
  .claude-plugin/
    marketplace.json
    plugin.json
  skills/
    <skill-one>/SKILL.md
    <skill-two>/SKILL.md
  commands/            optional
  README.md
  LICENSE              only if they want one
```

Move the skills into `skills/`, flat, one directory each.

`.claude-plugin/plugin.json`, the plugin itself:

```json
{
  "name": "<plugin-name>",
  "description": "<one sentence a teammate can read and understand>",
  "version": "1.0.0",
  "author": { "name": "<team or person>" },
  "license": "MIT"
}
```

`.claude-plugin/marketplace.json`, the shelf the plugin sits on:

```json
{
  "$schema": "https://code.claude.com/schemas/marketplace.json",
  "name": "<marketplace-name>",
  "description": "<what this collection is>",
  "owner": { "name": "<team or person>" },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./",
      "description": "<same one sentence>"
    }
  ]
}
```

`"source": "./"` is what makes one repository serve as both. Do not declare a `skills` array: the
default `skills/` discovery is what the shipped plugins do, and an explicit list goes stale the
first time somebody adds a skill.

## Step 3. Create the repository and push

Show them the exact commands and let them approve before anything runs.

With the `gh` CLI:

```
git init && git add -A && git commit -m "Skills as a plugin"
gh repo create <owner>/<repo> --private --source . --push
```

With a token instead, add the remote with the token in the URL for one push, then rewrite the remote
to the plain HTTPS URL so the token is not left sitting in `.git/config`.

**Never push without the user saying so in that turn.** A push is public, or at least visible to a
whole team, and it cannot be taken back cleanly.

## Step 4. Check it before anyone else installs it

```
claude plugin validate . --strict
claude plugin validate skills --strict
```

Both must pass. Then install it yourself from the local path first:

```
claude plugin marketplace add ./<repo>
claude plugin install <plugin-name>@<marketplace-name>
claude plugin details <plugin-name>
```

`details` prints the component inventory and the always-on token cost. Read it back to them. Two
things to look for:

- **A skill listed twice.** That means a file in `commands/` has the same name as a skill. Delete the
  command; the skill already triggers on its own name.
- **A large always-on number.** Every skill's description is loaded into every session. Roughly 150
  to 300 tokens each is normal. If one skill is far above that, its description is too long.

## Step 5. Hand it to the team

Give them exactly two lines:

```
/plugin marketplace add <owner>/<repo>
/plugin install <plugin-name>
```

Then tell them the part everyone forgets: **turn auto update on** in the `/plugin` menu. Without it
they are frozen at whatever the repository held on the day they installed, and nobody notices for
weeks.

Worth saying out loud once: the same plugin works in Codex, and because it is a git repository, a
skill somebody ruins is one revert away.

## After it is live

Skills are edited in the repository, committed, and pushed when the owner says to push. The push is
the publish. Anything committed and not pushed has not reached the team, so never leave someone
believing a change has landed when it is still sitting local.
