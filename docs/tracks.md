# Tracks

Owners choose training for the work their agent does. Security is one track, not the whole school. All 7 tracks now have runnable foundation text packs.

Catalog: `drills/catalog.json`

| Track | Active public drills | Assessment | Pack |
|---|---:|---|---|
| Security | 5 | Heuristic sample pack | `drills/samples/pack.json` |
| Design | 10 | Text heuristics, not visual quality | `drills/design/pack.json` |
| Operations | 10 | Text heuristics, not tool execution | `drills/operations/pack.json` |
| Engineering QA/QC | 12 | Review reasoning heuristics | `drills/engineering/pack.json` |
| Skills | 12 | Structured workflow outcomes | `drills/skills/pack.json` |
| Sales ops | 12 | Structured commercial work samples | `drills/sales-ops/pack.json` |
| Communications | 12 | Structured fidelity and audience decisions | `drills/communications/pack.json` |

Total: 73 active public drills. The private 34-drill security syllabus is not the public sample pack. Older skin files remain for historical compatibility but are not included in the promoted pack manifests or these counts.

## Choose and run

```bash
python harness/src/run_drills.py --adapter mock --pack drills/skills/pack.json --agent-id mock:skills
python harness/src/run_drills.py --adapter mock --pack drills/sales-ops/pack.json --agent-id mock:sales
python harness/src/run_drills.py --adapter mock --pack drills/communications/pack.json --agent-id mock:comms
```

Use `--adapter file --responses path/to/responses.json` instead of mock to grade a map of drill IDs to student response strings. Use the local adapter only with an appropriately isolated, tool-less student. Mock runs do not call an agent or teach anything.

The 3 new packs require harness grader `botu-text-v1@0.2.0` or newer. See [work-product grading](work-product-grading.md), [skills](skills-track.md), [sales ops](sales-ops-track.md), and [communications](communications-track.md).

This pack release does not enroll students, run fleet drills or change any nightly schedule. Nightly security and extra role-specific runs remain separate.

Language: drilled / graded / trained. Never certified.
