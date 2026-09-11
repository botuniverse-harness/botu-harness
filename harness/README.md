# Bot U Harness (v0.1)

Local trainer harness. Runs drill packs, grades responses, emits portable evidence.

## Owner enroll (no SSH)

Strangers run the harness themselves. See `docs/owner-enroll.md` and `scripts/run-local-owner.ps1`.
The studio remote adapter is for our dogfood fleet only.

## Quick start

```bash
python harness/src/run_drills.py --adapter mock
```

Outputs:
- `evidence/runs/<runId>.json` (portable evidence)
- `evidence/runs/<runId>.md` (report card)

## Adapters

- `mock` — deterministic self-test replies (CI / sanity)
- `file` — JSON map of `{ "drill-id": "agent reply text" }`
- `openclaw` — live local gateway via `openclaw agent` (inline in run_drills.py)
- `openclaw-remote` — optional remote gateway via env (`OPENCLAW_GATEWAY_URL` +
  token env *name*, never a token on argv). Not the stranger enroll path.
  Tests: `python harness/tests/test_remote_adapter.py` (mocked, no network).

## Rules

- Say drilled / graded / trained. Never certified.
- Evidence expires (default 90 days in v0.1).
