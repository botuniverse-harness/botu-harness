# Bot U harness

Open-source night-school trainer for **your** AI agent. You run it on your machine. We never SSH in.

Language: drilled / graded / trained. Never certified. Results expire.

Marketing: <https://university.botuniverse.ai>
Parent: <https://botuniverse.ai>

## Waitlist (paid drill feed + morning report)

Not billed yet. Write: [admissions@botu.university](mailto:admissions@botu.university?subject=Bot%20U%20Admission%20Request)

Auditor tier is this repo: free harness, sample drills, local report cards.

## Tracks

Owner picks a track. All 7 tracks now have runnable text packs: security samples (5), design (10), operations (10), engineering QA/QC (12), skills (12), sales-ops (12), and communications (12). See [tracks](docs/tracks.md).

Skills, sales-ops and communications check concrete work products, not keyword mentions. Their mock scores verify the grader, not a student's ability. These are foundation packs, not complete professional curricula or proof of reliable tool execution. See [grading limits](docs/work-product-grading.md).

```bash
python harness/src/run_drills.py --adapter mock --pack drills/design/pack.json
```

## Quick start

```bash
python harness/src/run_drills.py --adapter mock
python harness/tests/test_grader.py
python harness/tests/test_remaining_tracks.py
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
