# Investment Research

Repo backing a weekly Claude Code routine that scans markets and emails research leads.

## Architecture

```
Sunday 10:30 Madrid time
  └─→ Claude Code routine runs in Anthropic cloud
        ├─ Clones this repo
        ├─ Reads methodology/ and recent history/
        ├─ Web-searches macro + sectors + crypto + commodities + rates
        ├─ Writes history/YYYY-WNN.md with report + ## Email Digest block
        └─ Commits & pushes to main
              └─→ GitHub Actions (.github/workflows/email-digest.yml)
                    ├─ Detects new file under history/
                    ├─ Extracts the digest block via scripts/extract_digest.py
                    └─ Emails it via Gmail SMTP → your inbox
```

No servers, no cron, no always-on machine. Everything runs on Anthropic and GitHub infra.

## Structure

```
methodology/
  market-scan.md       # Sector + asset checklist
  thesis-building.md   # Structure required for each idea
  risk-framing.md      # Mandatory caveats block

history/
  YYYY-WNN.md          # Weekly reports, one per ISO week

scripts/
  extract_digest.py    # Pulls the digest section out of a report

.github/workflows/
  email-digest.yml     # GitHub Action: sends email on commit to history/
```

## One-time setup

### 1. Gmail App Password

1. Enable 2-factor auth on your Google account: https://myaccount.google.com/security
2. Generate an App Password: https://myaccount.google.com/apppasswords
   - Name it e.g. "GitHub investment-research"
   - Copy the 16-character password

### 2. GitHub repo secrets

In the repo → Settings → Secrets and variables → Actions → New repository secret:

- `GMAIL_USER` — your Gmail address (e.g. `you@gmail.com`)
- `GMAIL_APP_PASSWORD` — the 16-char App Password from step 1

The workflow sends email from this address to this address (to yourself).

### 3. Claude Code routine

At https://claude.ai/code/routines → New routine:

- **Prompt**: paste `ROUTINE_PROMPT.md`
- **Repository**: this repo, with "Allow unrestricted branch pushes" enabled
- **Trigger**: Weekly preset
- **Environment**: Default (network access needed for web search)

After saving, run `/schedule update` in the Claude Code CLI and set cron:
```
30 10 * * 0
```
(Sunday 10:30 local time.)

### 4. Test

Click **Run now** on the routine. Within ~5 minutes:
- A new `history/2026-WNN.md` should appear on `main`
- The email-digest workflow should run (check the Actions tab)
- An email should arrive in your inbox

If the email doesn't arrive, check:
- Spam folder
- Actions tab → the workflow run → logs
- That both secrets are set correctly

## Manual runs

- **From web**: routine detail page → Run now
- **From CLI**: `/schedule run <routine-name>`

## Changing behavior

Edit the methodology files (`market-scan.md`, `thesis-building.md`, `risk-framing.md`) and push. The next run picks up the changes automatically — no routine edit needed.

To change what's in the email, edit `scripts/extract_digest.py` or the `Email Digest` block format in `ROUTINE_PROMPT.md`.

## Reports are research, not advice

Every report includes the full block from `methodology/risk-framing.md`. These are leads for further investigation, not recommendations.
