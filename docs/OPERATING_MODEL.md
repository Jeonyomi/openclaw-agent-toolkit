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
