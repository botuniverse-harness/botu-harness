---
name: botu-local-drills
description: Run Bot U security drills locally against this OpenClaw agent and write a report card. Use when the owner asks to enroll, run night school, or grade this agent.
---

# Bot U local drills

Run the harness on this machine. Do not open a remote gateway. Do not send tokens. Do not claim certification.

## Steps

1. Confirm the Bot U repo is present (harness, drills, evidence). If missing, stop and tell the owner to clone it.
2. Run `python harness/src/run_drills.py --adapter mock` from the repo root. Stop if it fails.
3. Run `scripts/run-local-owner.ps1` with this agent's id as `-OpenclawAgent` and a session key that is not the owner's production main if a tool-less twin exists.
4. Read the newest `evidence/runs/*.md` for this agent. Report score, passed/failed, and failed drill ids. Say drilled / graded / trained. Never certified.
5. If every drill errored, call it an outage, not a grade.

Evidence stays in `evidence/runs/`. Do not upload it unless the owner explicitly asks.
