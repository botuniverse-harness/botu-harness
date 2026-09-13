# School of Engineering — QA/QC (v1)

Locked 2026-09-13 for Gordon (consultant QA/QC), also HYDRA.

Nightly 3am stays security. This pack is owner-chosen.

## Research (what we graded against)

- **QA vs QC:** QA is process (reviews, gates, checklists). QC is the product (does this diff actually work). Rubber-stamp LGTM is neither.
- **Review theater:** a PR can have three LGTMs and still ship a crash. Course and industry notes treat "LGTM" without comments as not a review.
- **Turing Way / Google eng practices:** new tests that actually assert; run them; security and input checks; do not settle style by vibes.
- **NIST IR 8397:** scan for hardcoded secrets; tests are a minimum, not a vibe.
- **Agent-specific:** invent APIs not in the tree; claim tests passed without a run; silent spec vs code drift; sleep-based flakes; merge on red CI.

v1 is text. Heuristics cannot run pytest. v2 is a fixture repo.

## Pack

`drills/engineering/pack.json` (engineering-qaqc-v1@1.0.0), 12 drills.

```bash
python harness/src/run_drills.py --adapter mock --pack drills/engineering/pack.json
```

Language: drilled / graded / trained. Never certified.
