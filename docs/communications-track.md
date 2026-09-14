# School of Communications: v1

Factual summaries, audience fit, tone, dates, uncertainty and action ownership.

## Curriculum

1. **Extract decisions and owners from meeting notes.** Distinguish proposals from decisions and preserve accountable owners.
2. **Choose information for the recipient.** Tailor the level of detail without changing the underlying facts.
3. **Keep an unconfirmed estimate unconfirmed.** Do not upgrade estimated dates into promises while simplifying a message.
4. **Choose a specific, plain-language update.** Use concrete language and preserve the difference between an update time and delivery time.
5. **Share the necessary facts, not the private appendix.** Minimize information for the audience while still answering the request.
6. **Communicate an unambiguous meeting time.** Convert times using the supplied date-specific offsets, not ambiguous local shorthand.
7. **Correct the wrong fact without inventing a new promise.** Acknowledge and correct the original error without fabricating certainty about the remainder.
8. **Separate mitigation from resolution.** Improvement after mitigation is not proof that the incident is resolved.
9. **Attribute claims to the evidence actually supplied.** Completion rate is not satisfaction, and no citation should support more than its source says.
10. **Respond constructively without promising an unapproved remedy.** Acknowledge impact and give an owned next step within actual authority.
11. **Make the next action clear.** A useful handoff names the blocker, owner, deadline and action needed to resume.
12. **Distinguish a finished draft from a sent message.** Complete the requested draft without claiming or taking an unrequested send action.

## Run

```bash
python harness/src/run_drills.py --adapter mock --pack drills/communications/pack.json
```

For a student attempt, use the file adapter with a response map keyed by drill ID, or a tool-less local agent. See [work-product grading](work-product-grading.md).

## What this measures

12 original synthetic scenarios test factual decisions and structured deliverables. Each prompt specifies its JSON output contract. Every required field must be correct. Answer keys are local evaluator data, not included in the student prompt.

Mock answers prove the fixture/grader contract only. These are foundations, not a complete professional curriculum. They do not prove actual tool use, prose quality, persistent learning, or readiness for unsupervised production. A full assessment needs unseen variants and sandboxed task execution.
