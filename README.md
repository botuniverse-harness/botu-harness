# Bot U harness

Open-source night-school trainer for **your** AI agent. You run it on your machine. We never SSH in.

Language: drilled / graded / trained. Never certified. Results expire.

Marketing: <https://university.botuniverse.ai>
Parent: <https://botuniverse.ai>

## Waitlist (paid drill feed + morning report)

Not billed yet. Write: [admissions@botu.university](mailto:admissions@botu.university?subject=Bot%20U%20Admission%20Request)

Auditor tier is this repo: free harness, sample drills, local report cards.

## Tracks

Owner picks a track. Security is the first live nightly pack. Design is a real text pack (non-AI tells + enterprise system). Other tracks are still **skins** (3 intro drills). See `docs/tracks.md` and `docs/design-track.md`.

```bash
python harness/src/run_drills.py --adapter mock --pack drills/design/pack.json
```

## Quick start

```bash
python harness/src/run_drills.py --adapter mock
python harness/tests/test_grader.py
```

Against a local OpenClaw agent (prefer a tool-less student twin, not production main):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-local-owner.ps1
```

See `docs/owner-enroll.md`.

Outputs:
- `evidence/runs/<runId>.json` portable evidence
- `evidence/runs/<runId>.md` report card

## What this is not

- Not a remote gateway into your agent
- Not a diploma or safety guarantee
- Not League, Exchange, or Agent ID (later)
- Not ads. No social campaign from this repo.

## License

MIT. Sample drills are the community syllabus. The weekly paid feed is separate.
