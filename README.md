# Investment Research

Repo backing a weekly Claude Code routine that scans markets and produces research leads.

## Structure

```
methodology/
  market-scan.md       # Sector + asset checklist
  thesis-building.md   # Structure required for each idea
  risk-framing.md      # Mandatory caveats block

history/
  YYYY-WNN.md          # Weekly reports, one per ISO week
```

## How it works

1. A Claude Code routine runs weekly (Sundays 09:00 Europe/Madrid).
2. The routine reads `methodology/` and the latest entries in `history/`.
3. It performs a macro + multi-asset scan via web search.
4. It commits a new `history/YYYY-WNN.md` back to this repo.
5. It sends a digest via the Telegram connector.

The routine prompt lives in the Claude Code routine config (not in this repo). Editing the methodology files here changes the agent's behavior on the next run without touching the prompt.

## Manual runs

To trigger a run outside the schedule: open the routine at claude.ai/code/routines and click "Run now", or use the per-routine API endpoint.

## Reports are research, not advice

Every report must include the full block from `methodology/risk-framing.md`. These are leads for further investigation, not recommendations.
