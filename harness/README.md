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
- `openclaw-remote` — live REMOTE gateway (`adapters/openclaw_remote.py`).
  Targets `OPENCLAW_GATEWAY_URL`/`OPENCLAW_GATEWAY_TOKEN` env contract via the
  official CLI. Token passed by ENV VAR NAME (`--gateway-token-env`, roster
  `gatewayTokenEnv`), resolved in-process (process env, then Windows user/machine
  scopes) so the value never appears on a command line, in logs, or in evidence.
  1 retry on transient disconnect or remote provider failure, hard timeout
  backstop (`--openclaw-timeout` + 90s) so a dead endpoint marks the drill
  `error` instead of hanging the run.
  Tests: `python harness/tests/test_remote_adapter.py` (mocked gateway, no network).
  Live smoke: `scripts/smoke-remote-gordon.ps1` (1 drill against Gordon).

## Rules

- Say drilled / graded / trained. Never certified.
- Evidence expires (default 90 days in v0.1).
