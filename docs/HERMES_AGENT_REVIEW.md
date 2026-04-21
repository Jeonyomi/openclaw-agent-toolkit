# HERMES Agent Review -> OpenClaw Toolkit Upgrade Notes

## Why review Hermes

`nousresearch/hermes-agent` is opinionated about something important:
- memory should stay compact and factual
- procedures should live in skills, not memory
- cross-session recall should come from session search / summaries
- skills should be actively maintained, not treated as static docs

That maps well to Billy's operating model.

## Hermes patterns worth adopting

### 1. Memory is for durable facts, not task logs
Hermes explicitly steers memory toward:
- user preferences
- environment facts
- stable conventions
- durable lessons

And steers it away from:
- temporary task progress
- completed-work logs
- TODO state
- imperative instructions

### 2. Skills are where reusable workflows belong
Hermes repeatedly pushes the agent to:
- save tricky/repeated workflows as skills
- patch skills when they are incomplete or stale
- treat outdated skills as liabilities

### 3. Recall should be separated from durable memory
Hermes distinguishes:
- **durable memory** -> compressed, stable facts
- **session search / summaries** -> historical work recall

For Billy/OpenClaw this implies:
- `MEMORY.md` and curated candidates should stay lean
- raw execution history should remain in session logs / daily notes
- toolkit outputs should prefer candidate generation over direct long-term writes

### 4. Prompt-safe recalled context matters
Hermes fences recalled memory context so the model does not confuse it with fresh user input.

OpenClaw already has its own mechanisms, but the toolkit should preserve the same philosophy:
- generated memory should be factual
- generated skills should be procedural
- generated outputs should be easy to review before reuse

### 5. Maintenance loop > one-shot generation
Hermes emphasizes:
- create skill after solving hard problem
- patch skill when real usage reveals missing steps
- measure usage/edits over time

This suggests the toolkit should optimize not only for generation, but for:
- draft review
- validation
- later refreshes

## Upgrades applied in this repo

### Memory capture
Upgraded to reject by default when content looks like:
- procedural instructions
- transient progress logs

This enforces a cleaner split:
- durable fact -> memory capture
- workflow/runbook -> skill draft

### Skill draft generation
Upgraded to produce richer draft structure:
- `## When to use`
- `## Steps`
- `## Validation`
- `## Cautions`
- `## Status`
- `## Maintenance notes`

Also added:
- comma-joined step splitting
- explicit draft metadata for validations/source

### Validation
Upgraded validator now checks for:
- imperative memory entries
- transient/progress-like memory outputs
- missing skill sections
- malformed comma-joined skill steps

## Recommended Billy operating model

### Capture to memory when the output is a durable fact
Examples:
- "MJ prefers X"
- "Default recovery path is service-based gateway restart"
- "Project Y is intentionally paused"

### Capture to skill when the output is a repeatable workflow
Examples:
- recovery sequence
- repo bootstrap flow
- scheduler audit flow
- integration/debugging runbook

### Do not put into durable memory
Examples:
- "tests passed today"
- "next step is to refactor file X"
- "blocked on quota right now"
- detailed one-off command transcripts

## Next upgrades worth considering

1. Add a local `recall-candidate` helper for distilling daily notes into MEMORY candidates
2. Add `skill-refresh` to compare live skills against new lessons learned
3. Add simple usage telemetry for generated/promoted drafts
4. Add a review queue file so Billy can periodically revisit draft skills
