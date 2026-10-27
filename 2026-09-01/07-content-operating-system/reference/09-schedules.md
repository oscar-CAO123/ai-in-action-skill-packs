# Phase 8. The two scheduled tasks

The system only produces two scheduled tasks. Everything else runs when a person asks for it.

| Task | Default schedule | What it does | Unattended? |
|---|---|---|---|
| **Ingestion** | Daily, 03:00 local | Pulls every enabled source since the last watermark, redacts, normalises, writes to the evidence store | Yes |
| **Ideation** | Weekly, the morning before their planning day | Reads the store, clusters, ranks, writes the dated idea queue and the review page, refreshes the founder question bank | Yes |

**Production is not scheduled.** It runs when the operator picks something out of the queue. That is
deliberate: production is where the money and the publishing risk sit, so it stays attached to a
person.

---

## Which scheduler to use

Detect first, then choose. In this order.

### 1. The running agent's own scheduler

If the agent you are running in has a native scheduled task, routine, or cron capability, use it.
This is the best option because the task runs inside the agent, with its context and its tools, and
it survives the agent's own updates.

**How to find out:** check your own available tools and settings for a scheduling capability. Do not
guess from the product name, and do not claim a capability you have not confirmed. Different builds
of the same agent ship different tools.

If you have one, create both tasks through it, with:

- A name that says what it is: `cos-ingest`, `cos-ideate`.
- The instruction to run `engine/run-ingest.sh` or `engine/run-ideate.sh` from the project root.
- The schedule from interview questions 85 and 86.

Then tell the operator, in one line each, what was created and how they remove it.

### 2. The agent's headless mode, driven by the OS scheduler

If the agent has no native scheduler but does have a non-interactive mode, this is the next best
thing, and it is the most portable option in the pack. The OS wakes up, calls the agent headless, and
the agent does the work with its full context.

Confirm the headless invocation by **running it once**, not by assuming the flag. Common shapes:

```bash
claude -p "read engine/AGENT-INGEST.md and follow it"
codex exec "read engine/AGENT-INGEST.md and follow it"
gemini -p "read engine/AGENT-INGEST.md and follow it"
```

Whatever works, put it inside `engine/run-ingest.sh` so the scheduler only ever calls one path.

### 3. Plain Python, driven by the OS scheduler

The fallback that always works. Ingestion is almost entirely deterministic and does not need a model
at all, so on most setups this is the right choice for ingestion regardless.

```bash
cd "$PROJECT_ROOT" && python3 -m cos.ingest
```

Ideation does need judgement, so it calls the agent from inside the Python run, through
`cos/agent.py`. If no agent CLI is reachable, ideation degrades to rule-based ranking, writes the
queue with a banner saying the judgement pass did not run, and tells the operator what to run by
hand. It never silently produces a worse queue without saying so.

---

## Installing on the OS

### macOS, launchd

Preferred over `crontab` on macOS, because launchd runs a missed job when the machine wakes and cron
does not. A laptop that sleeps at 03:00 never runs a 03:00 cron job, which is the most common reason
these systems appear to be broken.

`~/Library/LaunchAgents/com.cos.ingest.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.cos.ingest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>cd PROJECT_ROOT &amp;&amp; ./engine/run-ingest.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>3</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>PROJECT_ROOT/outputs/logs/ingest.log</string>
  <key>StandardErrorPath</key><string>PROJECT_ROOT/outputs/logs/ingest.err</string>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
```

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cos.ingest.plist
launchctl kickstart -k gui/$(id -u)/com.cos.ingest   # fire it once now, to prove it works
launchctl print gui/$(id -u)/com.cos.ingest | head -20
```

To remove: `launchctl bootout gui/$(id -u)/com.cos.ingest && rm ~/Library/LaunchAgents/com.cos.ingest.plist`

Substitute `PROJECT_ROOT` with the real absolute path. Repeat for `com.cos.ideate` with the weekly
schedule, using `StartCalendarInterval` with a `Weekday` key.

**Full disk access.** If the sources include folders under Drive, Dropbox, iCloud, Documents or
Desktop, the scheduled job needs Full Disk Access granted to whatever binary runs it, in System
Settings, Privacy and Security. Without it the job runs and silently finds nothing, which is the
second most common reason these appear broken. Tell them before it happens, not after.

### Linux, cron or systemd

```
0 3 * * *   cd PROJECT_ROOT && ./engine/run-ingest.sh >> outputs/logs/ingest.log 2>&1
0 8 * * 1   cd PROJECT_ROOT && ./engine/run-ideate.sh >> outputs/logs/ideate.log 2>&1
```

On a machine that sleeps, use a systemd timer with `Persistent=true` instead.

### Windows, Task Scheduler

```
schtasks /create /tn "cos-ingest" /tr "powershell -c \"cd 'PROJECT_ROOT'; .\engine\run-ingest.ps1\"" /sc daily /st 03:00
schtasks /create /tn "cos-ideate" /tr "powershell -c \"cd 'PROJECT_ROOT'; .\engine\run-ideate.ps1\"" /sc weekly /d MON /st 08:00
```

Tick "Run task as soon as possible after a scheduled start is missed" in the task's settings, for the
same sleep reason.

---

## What the runner scripts must do

Both `run-ingest.sh` and `run-ideate.sh` are written by the build. Both must:

1. **Resolve their own project root** rather than depending on the working directory. A scheduler
   starts a job in a directory you did not choose.
2. **Load `.env` from the project root**, and only the variables that run needs.
3. **Use an absolute path to `python3`.** A scheduled job gets a minimal environment with a different
   `PATH`, and `python3: command not found` at 03:00 is the third most common failure here.
4. **Take a lock** so two runs never overlap. A lock file with the pid, checked and cleared on exit.
5. **Write a run record** to `outputs/logs/` with the start time, per-source counts, the end time and
   the exit code.
6. **Exit non-zero on failure**, so the log shows a real failure rather than a quiet no-op.
7. **Never publish, never send, never spend.** These two jobs read and write local files. That is the
   whole scope, and it is what makes them safe to run unattended.

---

## Proving it works, before you say it is installed

Do all four. Do not report the schedule as installed until they have passed.

1. Run the script by hand from the project root. It should complete and write a log.
2. Run it by hand from a different directory, with `cd / && PROJECT_ROOT/engine/run-ingest.sh`. This
   catches every path assumption at once.
3. Trigger it through the scheduler itself, immediately, rather than waiting for 03:00.
4. Read the log file it produced and confirm the per-source counts are non-zero for at least one
   source.

If step 4 shows zeros everywhere, the schedule is fine and the source wiring is not. Go back to
`08-connections.md` rather than adjusting the schedule.

---

## What to tell the operator when it is done

Four lines, no more:

- What is installed, when each runs, and where the logs go.
- The one command to run each by hand.
- The one command to remove each.
- The one thing most likely to break it, which is either the token expiry from
  `08-connections.md` or the disk access permission above.
