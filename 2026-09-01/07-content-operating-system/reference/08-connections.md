# Phase 4. Connections

Some of what this system needs is already reachable. The rest needs credentials, and this is the
phase where you either get them or write down honestly that you did not.

Two rules govern the whole phase.

**Check for an existing connection first.** An MCP server, a wired connector, an already-authenticated
CLI or an existing token in their environment beats setting up a new integration every time. Run the
detection below before you ask anyone to create an app.

**The operator handles their own credentials.** You tell them exactly what to create, which scopes to
tick, and which variable name to store it under. They paste it into their `.env` themselves. You
never ask them to send you a key in chat, and you never write one into a file.

---

## Detection, before anything else

```
1. MCP config: .mcp.json, .cursor/mcp.json, ~/.codex/config.toml, the Claude Code settings file.
   Any mcpServers entry for a platform means it may already be reachable. Try a read call.
2. Authenticated CLIs: gh auth status, gcloud auth list, aws sts get-caller-identity,
   supabase projects list, stripe config --list. Whatever is installed, ask it who it is.
3. Environment: env | grep -iE 'TOKEN|KEY|SECRET' | cut -d= -f1
   Names only, never values. A name tells you the connection exists.
4. .env.example or a config template, which lists what the project expects to exist.
```

Report what is already reachable in two lines, then only walk through setup for what is missing and
actually needed.

---

## The credential home

Decided in interview question 83.

If they have a convention, use it. If they do not:

```bash
# at the project root
touch .env
printf '.env\n.env.*\n!.env.example\n' >> .gitignore
git check-ignore .env    # must print .env before anything is committed
chmod 600 .env
```

Then write `.env.example` with **variable names only, no values**, and commit that instead.

`engine/config.json` never holds a secret. It holds the variable name:

```json
{ "id": "reviews_google", "type": "reviews", "token_env": "GOOGLE_PLACES_API_KEY" }
```

If `git check-ignore .env` does not print `.env`, stop and fix it before continuing. A key in a
tracked file is the one mistake in this build that cannot be undone by editing a file, because the
key has to be rotated.

---

## Per-platform setup

Only walk through the ones the interview actually selected. Each one ends with a **verify** step, and
an unverified connection is written into the register as unverified.

### Meta (Instagram, Facebook, ads)

Reading their own organic Instagram and Facebook content needs a Business account, a connected Page,
and an app.

1. developers.facebook.com, create an app, type Business.
2. Add the Instagram Graph API and Facebook Login for Business products.
3. Connect the Instagram professional account to the Facebook Page. Personal Instagram accounts
   cannot be read at all, and this is where most setups stop.
4. Scopes for reading their own content: `instagram_basic`, `pages_read_engagement`,
   `pages_show_list`, `instagram_manage_insights`.
5. Generate a long-lived token, sixty days, and note the expiry in the register. This one will break
   and somebody has to know why.
6. Ads reading additionally needs `ads_read` and the ad account id in the form `act_<digits>`.

- **Store as:** `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_AD_ACCOUNT_ID`.
- **Verify:** `GET /v21.0/{ig-user-id}/media?fields=id,caption,timestamp&limit=1`.
- **Warning to give them, plainly:** ad account access is sensitive and automated pulls against it
  can trigger review. Read only, at low frequency, and only if they asked for it.

### TikTok

1. developers.tiktok.com, create an app, apply for Login Kit and Display API.
2. Approval takes days. Say that up front so it does not look like a failure.
3. Scopes: `user.info.basic`, `video.list`.

- **Store as:** `TIKTOK_ACCESS_TOKEN`, `TIKTOK_OPEN_ID`.
- **Verify:** `GET /v2/user/info/?fields=open_id,display_name`.
- **Note:** posting through the API needs additional review. Treat TikTok as read-only.

### LinkedIn

1. linkedin.com/developers, create an app, associate it with the Company Page they administer.
2. Products: Share on LinkedIn, and Community Management API for organisation analytics.
3. Personal profile analytics are not available through the API at all. Only the Company Page is.
   Tell them this before they spend an hour on it.

- **Store as:** `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_ORG_URN`.
- **Verify:** `GET /rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={urn}`.

### YouTube

1. Google Cloud console, new project, enable the YouTube Data API v3.
2. An API key is enough for public read. OAuth is only needed for their own analytics.

- **Store as:** `YOUTUBE_API_KEY`, and `YOUTUBE_CHANNEL_ID`.
- **Verify:** `GET /youtube/v3/channels?part=statistics&id={channel}&key={key}`.

### Reddit

Public JSON endpoints need no key for the volumes this system uses. Set a real user agent and stay
under one request per two seconds.

For higher volume: reddit.com/prefs/apps, create a script app, use the client credentials flow.

- **Store as:** `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`.
- **Verify:** fetch one listing from one of the subreddits they named in interview question 74.

### X

There is no free read tier worth using. Their options are the paid API tier, an existing search tool
they already pay for, or manual collection.

Do not build around it if they are not already paying. Register it as a gap and move on.

- **Store as:** `X_BEARER_TOKEN` if they have one.

### Google reviews

1. Google Cloud console, enable the Places API for competitor and public reviews, or the Business
   Profile API for their own.
2. Places returns a limited number of reviews per place. It is enough to start.

- **Store as:** `GOOGLE_PLACES_API_KEY`.
- **Verify:** a place details call for their own listing.

### Helpdesk

Intercom, Zendesk, Front, Help Scout, Freshdesk and Crisp all follow the same shape: settings,
developers or API, create a token, read scopes only.

- **Store as:** `HELPDESK_API_TOKEN`, plus `HELPDESK_SUBDOMAIN` for Zendesk and Freshdesk.
- **Verify:** list one conversation from the last thirty days.
- **Faster alternative:** a CSV export. Zero credentials, works today, and for the first run it is
  the better choice. Wire the API once the loop is proven.

### CRM

HubSpot uses a private app token with read scopes. Pipedrive and Close use an API key from settings.
Attio uses an access token. Salesforce needs a connected app and usually an admin.

- **Store as:** `CRM_API_TOKEN`.
- **Verify:** read one deal or contact and confirm the notes or lost-reason field is populated.
- **The finding that matters:** if the notes field is empty across the last twenty deals, the CRM is
  not an evidence source, it is a database of names. Say so and rank it accordingly.

### Call recording

Fathom, Granola, Fireflies, Otter, Grain and tl;dv each have either an export destination setting or
an API.

**Always prefer the export destination.** Point it at a folder, and the ingestion job watches the
folder. No token, no expiry, no rate limit, and it keeps working when the vendor changes their API.

- **Store as:** `CALLS_API_TOKEN` only if there is no export path.
- **Verify:** the folder exists and contains at least one transcript from the last thirty days.

---

## Writing the connection register

Every connection, wired or not, gets a row in `brain/source-register.md`:

| Field | Example |
|---|---|
| Platform | Instagram |
| Status | wired and verified / wired unverified / blocked / not needed |
| Reached by | Meta Graph API, long-lived token |
| Variables | `META_ACCESS_TOKEN`, `META_IG_USER_ID` |
| Expires | 2026-10-30, sixty days |
| Verified | 2026-09-01, one media item returned |
| Unlocks | own-channel performance for the ideation ranking |
| Blocked by | nothing / awaiting app review / admin approval needed |

A `blocked` row is a real deliverable. It tells them what to chase and what it would buy them, which
is more useful than a connection quietly missing.

---

## What never happens in this phase

- No key is written to a tracked file, a config file, a script, or a chat message.
- No write scope is requested when a read scope will do.
- No posting or publishing permission is set up in this build at all. This system produces content
  and stops at a person. Publishing access is a separate decision on a separate day.
