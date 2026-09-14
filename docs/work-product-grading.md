# Work-product grading

Skills, sales-ops and communications v1 use `botu-text-v1@0.2.0` and synthetic,
text-only work samples. The existing four tracks retain their heuristic checks.
Use the matching harness revision; older versions do not understand this schema.

## Contract

Each student prompt states the scenario, rules, available choices, field names,
types and ordering. It asks for one JSON object. The drill's evaluator-only
`expected.json_answer` specifies the complete expected result. Object key order
and whitespace do not matter. An outer JSON Markdown fence is accepted.
Arrays must follow the ordering stated in the prompt. Integer quantities are
integers, not strings or booleans. Missing, duplicate or extra fields, unsupported
claims and malformed output fail. One incorrect required field fails the drill;
field-level notes identify what needs review. Scores are 100 or 0 per drill.

Example contract: report `verified` and `unexplained_missing_rows` after comparing
120 eligible input rows with 117 output rows and no documented exclusions.
Saying "verified" is not enough: the student must report `false` and `3`.

No student is asked to install software, send a message, alter a calendar or touch
production. All people, dates, quantities and companies in these fixtures are
synthetic. Scenarios describe actions for analysis, not authorization to execute.

## Validation

```bash
python harness/tests/test_remaining_tracks.py
python harness/tests/test_grader.py
python harness/tests/test_remote_adapter.py
python harness/src/run_drills.py --adapter mock --pack drills/skills/pack.json
```

There is a manually authored plausible incorrect response for every new drill.
Checks also exercise empty answers, keyword-only refusals, omitted fields,
reordered valid objects, fenced responses, duplicate keys and JSON type errors.
The legacy skin generator stops before overwriting promoted packs.

## Interpretation and limits

Mock scores measure fixture wiring only, not a student's ability. Public answer
keys are useful for transparent practice, not a hidden benchmark. A student with
access to this repository can memorize them. Do not give students the answer-key
file; use unseen variants for meaningful assessment.

Passing shows accurate structured answers on these fixtures. It does not measure
writing quality, design taste, executed tool behavior or persistent improvement.
Repeated evaluation alone does not modify model weights or teach lasting skills.
Learning needs an explicit feedback/remediation loop and a later unseen retest.
Keep this text score separate from later artifact, human or sandbox-execution
reviews. Do not compare its percentage directly with older heuristic scores.
