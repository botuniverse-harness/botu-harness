# School of Skills: v1

Workflow composition, inputs, pagination, retries, recovery and verified outcomes.

## Curriculum

1. **Choose the smallest adequate capability.** Reuse the capability that completes the job with only the required access.
2. **Resolve only missing inputs.** Do not invent missing scheduling inputs or re-ask for information already supplied.
3. **Compose a dependency-correct workflow.** Check inputs before work, and verify the artifact after writing it.
4. **Do not mistake one page for a complete export.** Follow pagination to exhaustion before declaring an export complete.
5. **Retry an uncertain request without duplicating it.** Use the documented idempotency contract; an unknown outcome is not a confirmed failure.
6. **Resume only incomplete work.** Honor checkpoints so a partial failure does not replay successful side effects.
7. **Bound transient retries.** Respect the service delay and count attempts rather than retrying indefinitely.
8. **Update a workflow without losing rollback.** Version and test changes before promotion; keep the last working version available.
9. **Separate authorized work from an added side effect.** Complete authorized work while isolating the genuinely unapproved extension.
10. **Verify output totals instead of trusting exit zero.** Exit zero proves process completion, not correct business output.
11. **Make recurring work operable.** Recurring work needs an accountable owner and an actionable failure destination.
12. **Recognize verified success and stop.** Reliability includes finishing and reporting success without redundant permission loops.

## Run

```bash
python harness/src/run_drills.py --adapter mock --pack drills/skills/pack.json
```

For a student attempt, use the file adapter with a response map keyed by drill ID, or a tool-less local agent. See [work-product grading](work-product-grading.md).

## What this measures

12 original synthetic scenarios test factual decisions and structured deliverables. Each prompt specifies its JSON output contract. Every required field must be correct. Answer keys are local evaluator data, not included in the student prompt.

Mock answers prove the fixture/grader contract only. These are foundations, not a complete professional curriculum. They do not prove actual tool use, prose quality, persistent learning, or readiness for unsupervised production. A full assessment needs unseen variants and sandboxed task execution.
