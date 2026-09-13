# Tracks

Owner picks a track. Security is the first live pack, not the whole school.

Catalog: `drills/catalog.json`

| Track | Status | Pack |
|---|---|---|
| Security | live (34 drills in the lab pack) | `drills/samples/pack.json` |
| Skills | skin (3 intro) | `drills/skills/pack.json` |
| Engineering | v1 QA/QC text (12 drills, Gordon lane) | `drills/engineering/pack.json` |
| Design | v1 text (10 drills: non-AI tells + enterprise system) | `drills/design/pack.json` |
| Sales ops | skin | `drills/sales-ops/pack.json` |
| Communications | skin | `drills/communications/pack.json` |
| Operations | v1 text (10 drills: confirm, no fake done, no double-send) | `drills/operations/pack.json` |

Skin means a few graded intro drills, not a full term. Nightly dogfood stays on security until an outsider enrolls.

```bash
python harness/src/run_drills.py --adapter mock --pack drills/design/pack.json
```

Language: drilled / graded / trained. Never certified.
