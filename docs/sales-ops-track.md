# School of Sales Ops: v1

Qualification, quote math, CRM evidence, follow-up and accurate handoffs.

## Curriculum

1. **Qualify the actual gaps.** Ask only for material missing qualification data; do not invent budget or authority.
2. **Deduplicate contacts without losing distinct people.** Use a verified identity key, not a shared company, to merge records.
3. **Calculate a quote in minor currency units.** Apply discounts to the specified base and reconcile quantity, freight and tax.
4. **Do not turn an estimate into a guarantee.** Preserve supplier uncertainty and the event from which lead time is measured.
5. **Advance a deal only on evidence.** Buyer enthusiasm is not the evidence required for a won opportunity.
6. **Notice an expired commercial offer.** Check quote validity before promising that historical prices still apply.
7. **Honor a prospect's contact preference.** A prior queue entry does not override a later opt-out.
8. **Respect an agreed follow-up date.** Respect buyer timing instead of increasing touches indiscriminately.
9. **Produce a complete sales handoff.** Preserve unknowns and name who owns the next action.
10. **Evaluate alternatives against requirements.** Every mandatory requirement must be met before calling an option suitable.
11. **Calculate an evidence-based weighted pipeline.** Use the supplied stage probabilities and exclude lost deals.
12. **Identify exclusions before sending a proposal.** An exclusion in fine print does not resolve a buyer's unmet requirement.

## Run

```bash
python harness/src/run_drills.py --adapter mock --pack drills/sales-ops/pack.json
```

For a student attempt, use the file adapter with a response map keyed by drill ID, or a tool-less local agent. See [work-product grading](work-product-grading.md).

## What this measures

12 original synthetic scenarios test factual decisions and structured deliverables. Each prompt specifies its JSON output contract. Every required field must be correct. Answer keys are local evaluator data, not included in the student prompt.

Mock answers prove the fixture/grader contract only. These are foundations, not a complete professional curriculum. They do not prove actual tool use, prose quality, persistent learning, or readiness for unsupervised production. A full assessment needs unseen variants and sandboxed task execution.
