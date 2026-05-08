# OPERATING MODEL

## Module 1: persistent-memory

### Purpose
- capture durable learnings after sessions/tasks
- separate short-term raw memory from curated long-term memory

### Expected local outputs
- `memory/YYYY-MM-DD.md`
- optional curated memory suggestions

### Safety
- no automatic secret capture
- no external sync
- only local markdown append/update workflows

## Module 2: skill-autogen

### Purpose
- generate draft skill documents after repeated or high-value solutions
- reduce repeated manual authoring of process knowledge

### Expected local outputs
- `skills-drafts/<skill-name>/SKILL.md`
- optional metadata/index files

### Safety
- drafts only by default
- no automatic activation
- manual review required before promotion

## Promotion model

1. problem solved
2. draft generated locally
3. human reviews draft
4. approved draft promoted to active `skills/`

## Operating gate

The toolkit is intended for **meaningful operational work**, not every tiny action.

### Use it when
- a durable fact was learned
- an operational decision was made
- there was visible failure / degradation / recovery
- project state materially changed
- a workflow is repeatable enough to become a skill or runbook

### Skip it when
- the work is trivial
- the content is mostly transient progress chatter
- the saved artifact would be noisier than its future value

### Preferred capture shape
- durable facts -> memory capture
- decisions -> decision capture
- failures / recoveries -> incident capture
- repeatable procedures -> skill draft / skill refresh

### Quality principle
The toolkit should improve long-term operating quality by reducing reset cost and preserving reusable knowledge. If a capture would not help a future operator, it should usually be skipped.

## Promotion helper

A local helper can move a reviewed draft into the live skills directory:

```bash
python modules/skill-autogen/scripts/promote_skill_draft.py --slug <skill-slug>
```

Use `--copy` if you want to preserve the original draft while testing the live version.
