# Owner enroll (local-first)

This is the inversion. The owner runs the harness. Bot U does not SSH into their gateway.

Language: drilled / graded / trained. Never certified.

## What you install

The open harness in this repo. It talks to *your* OpenClaw agent on *your* machine, writes evidence next to the repo, and stops.

You do not give us a gateway URL or token.

## 1. Prove the grader

From the repo root:

```bash
python harness/src/run_drills.py --adapter mock
python harness/tests/test_grader.py
```

Mock must emit `evidence/runs/*.json` and `*.md`. Grader tests must stay green.

## 2. One-drill smoke against your agent

Point at a **tool-less student twin** if you have one (we use `botu-student` so production main is never the drill target). Otherwise use a session that cannot send mail, run exec, or write files.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-local-owner.ps1
```

Defaults: enroll smoke pack (`sec-hy-004` only), local `openclaw` adapter, session `agent:main:botu-drill`.

Override:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-local-owner.ps1 `
  -OpenclawAgent botu-student `
  -SessionKey agent:botu-student:botu-drill `
  -AgentId openclaw:my-agent `
  -AgentLabel "My agent"
```

Full pack later:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-local-owner.ps1 -FullPack
```

## 3. What you should see

- A report card under `evidence/runs/`
- Score over graded drills only. Adapter errors are outages, not F's
- No gateway token on any command line

## 4. What is not this yet

- Paid drill feed pull
- Uploading evidence to Bot U
- Stripe / morning Discord delivery for strangers
- Remote `openclaw-remote` adapter (that is our studio lab, not the product)

If this smoke works on a machine we do not SSH into, enrollment is inverted.
