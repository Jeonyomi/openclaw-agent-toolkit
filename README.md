# openclaw-agent-toolkit

Reusable local toolkit for OpenClaw agents across multiple PCs.

## What this repo is for

`openclaw-agent-toolkit` adds **local-first, update-independent memory and workflow helpers** on top of OpenClaw.

The design goal is simple:
- keep OpenClaw core untouched
- keep agent enhancements in a separate repo
- keep sensitive runtime state local
- make useful agent behaviors portable across machines and agents

This repo is for people who want their OpenClaw agents to do more than just chat.
It helps agents:
- capture durable memory
- record operational decisions
- record incidents and resolutions
- generate and refresh draft skills
- gather prior evidence before risky work
- review/promote memory and skill outputs in a controlled way

---

## Current capabilities

The toolkit currently supports:

### Memory and operations
- **durable memory capture**
- **structured decision capture** (`what / why / how / outcome`)
- **structured incident capture** (`symptoms / cause / resolution / related items`)
- **local evidence brief generation** across memory, incident, decision, and skill files
- **curated memory candidate review/apply flow**

### Skills and workflow reuse
- **draft skill generation**
- **existing skill refresh draft generation**
- **manual draft promotion**
- **validation and quality checks**

### Agent integration
- **Billy pilot helper**
- **generic agent rule snippets** for reuse on other PCs
- **bootstrap/install flow** for local layout setup

---

## Core operating model

This toolkit uses a practical split:

### 1. Durable memory
For facts worth keeping across sessions.
Examples:
- preferences
- stable project state
- durable lessons
- compact factual notes

### 2. Decisions
For important choices that need rationale.
Examples:
- what was decided
- why it was decided
- how it should be applied

### 3. Incidents
For failures, outages, repeated mistakes, or operational surprises.
Examples:
- symptoms
- cause or hypothesis
- resolution
- related skills or decisions

### 4. Skills
For reusable procedures or runbooks.
Examples:
- recovery workflows
- repo workflows
- scheduler operations
- deployment or debugging playbooks

### 5. Evidence / review
Before risky work, gather prior evidence first.
Examples:
- past decisions
- incidents
- memory entries
- live skills / draft skills

This means:
- transient progress logs should **not** go into durable memory
- TODOs/blockers should **not** go into durable memory
- reusable procedures should usually become **skills**, not memory
- failures and operational surprises should usually become **incidents**
- important operational choices should usually become **decisions**

---

## Fastest path to real operation on another PC

If your goal is not just to read the docs but to make another OpenClaw agent PC actually usable, follow this path.

### What “operational” means here

A PC should only be treated as operational after all of these are true:
- the repo is cloned locally
- local layout has been bootstrapped
- the local agent has rules telling it when to use the toolkit
- the machine has a usable command path or wrapper for post-task capture
- at least one real end-to-end validation run has succeeded
  - capture memory
  - generate curated candidate output
  - apply reviewed memory into local workspace files

### Important distinction

Updating docs in GitHub helps another user understand the process, but it does **not** by itself activate another PC.
A second PC becomes operational only when its own local repo, local instructions, local command/wrapper path, and local validation are all in place.

### 30-minute onboarding path for another PC

1. Clone this repo on that machine
2. Review `docs/SECURITY.md`
3. Run:

```bash
python scripts/bootstrap_local_layout.py
```

4. Decide how the local agent will call the toolkit:
   - direct `toolkit.py` commands
   - `scripts/post_task_capture.py`
   - a local wrapper/alias for Billy-like post-task behavior
5. Copy the generic rules from `docs/AGENT_RULE_SNIPPETS.md` into the local agent instruction file
6. Run one real validation flow on that machine
7. Only then treat the PC as pilot-operational

### Two common onboarding modes

#### Mode A — Generic agent on another PC

Use this when the other machine is not specifically trying to copy Billy's behavior.

Recommended starting commands:
- `memory-capture`
- `decision-capture`
- `incident-capture`
- `evidence-brief`
- `skill-draft`
- `skill-refresh`
- `recall-candidate`

#### Mode B — Automatic post-task capture mode

Use this when you want the agent to automatically capture durable memory after meaningful completed work instead of relying only on manual command use.

Minimum requirements:
- toolkit repo present locally
- local agent rules updated
- local wrapper or equivalent scripted command path available
- reviewed apply flow into that machine's `MEMORY.md` and `memory/YYYY-MM-DD.md`
- one successful end-to-end validation run

## Quick start

### 1. Bootstrap local layout

```bash
python scripts/bootstrap_local_layout.py
```

### 2. Capture a durable memory

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for OpenClaw recovery" \
  --source "OpenClaw recovery work"
```

### 3. Capture a structured decision

```bash
python toolkit.py decision-capture \
  --what "Use service-based gateway restart as the default recovery path" \
  --why "In-process restart can appear hung during drain/shutdown timeout" \
  --how "Prefer service-based restart in docs and operator workflow" \
  --source "OpenClaw recovery work"
```

### 4. Capture an incident

```bash
python toolkit.py incident-capture \
  --title "OpenClaw in-process restart looked hung" \
  --symptom "Gateway appeared stuck during shutdown" \
  --symptom "Agent responsiveness dropped during restart attempt" \
  --cause "In-process restart can wait on drain/shutdown timeout" \
  --resolution "Use service-based gateway restart instead" \
  --source "OpenClaw recovery work"
```

### 5. Gather evidence before risky work

```bash
python toolkit.py evidence-brief --query "gateway restart recovery"
```

### 6. Generate a draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

### 7. Refresh an existing skill with new lessons

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

### 8. Preview curated memory candidates

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### 9. Apply curated memory candidates into workspace memory files

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

### 10. Validate outputs before promotion

```bash
python scripts/validate_toolkit_outputs.py
```

### 11. Promote a reviewed draft skill

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

---

## Recommended usage flow after meaningful work

After a meaningful task is completed:

1. **If the outcome is a durable fact** → use `memory-capture`
2. **If the outcome is an important operational decision** → use `decision-capture`
3. **If the outcome is a failure / outage / repeated mistake** → use `incident-capture`
4. **If the outcome is a repeatable workflow** → use `skill-draft` or `skill-refresh`
5. **If curated memory candidates have accumulated** → review with `recall-candidate`, then `--apply`
6. **Before promoting draft skills** → run validation
7. **Before risky debugging or recovery work** → optionally run `evidence-brief`
8. **Promotion stays manual**

### Practical judgment hints

Use the smallest fitting capture:

- If the important part is **the durable fact** → `memory-capture`
- If the important part is **what was decided and why** → `decision-capture`
- If the important part is **what went wrong and how it was fixed** → `incident-capture`
- If the important part is **what should be reused next time** → `skill-draft` or `skill-refresh`

---

## For other users / another PC

If you want to use this repo on another PC or with another OpenClaw agent, this is the recommended path.

## Installation + activation steps

1. Clone the repo
2. Review `docs/SECURITY.md`
3. Run:

```bash
python scripts/bootstrap_local_layout.py
```

4. Review the generated local config files:
- `~/.openclaw/local-config/persistent-memory.local.json`
- `~/.openclaw/local-config/skill-autogen.local.json`

5. Keep generated outputs local:
- `~/.openclaw/workspace/MEMORY.md`
- `~/.openclaw/workspace/memory/*.md`
- `~/.openclaw/skills-drafts/*`
- toolkit output folders under local workspace/runtime directories

6. Copy the generic integration rules from:
- `docs/AGENT_RULE_SNIPPETS.md`

into your local agent instruction file if you want behavior-level integration.

7. Choose a local execution path for post-task usage:
- call `toolkit.py` directly
- call `scripts/post_task_capture.py`
- add a local wrapper or alias for your preferred operating style

8. Validate one real end-to-end path on that machine:
- capture a durable memory or decision
- confirm candidate output was generated
- preview with `recall-candidate`
- apply into local workspace memory files

9. Only after that should the machine be treated as operational.

---

## First validation flow for another PC

If you want a concrete first-run check, this is the simplest useful validation path.

### 1. Create one durable memory candidate

```bash
python toolkit.py memory-capture --type preference --text "The user prefers short operational updates." --source "first onboarding validation"
```

### 2. Preview the generated curated candidate

```bash
python toolkit.py recall-candidate --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### 3. Apply it into local workspace files after review

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

### 4. Confirm the result

Check that both of these now reflect the reviewed entry:
- `~/.openclaw/workspace/MEMORY.md`
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md`

If this flow works, the machine is no longer just installed — it is actually wired for basic toolkit operation.

## Minimal usage guide for another user

If you are not using Billy specifically and just want the toolkit patterns:

### Capture durable memory

```bash
python toolkit.py memory-capture --type decision --text "..." --source "agent work"
```

### Capture a decision

```bash
python toolkit.py decision-capture --what "..." --why "..." --how "..." --source "agent work"
```

### Capture an incident

```bash
python toolkit.py incident-capture --title "..." --symptom "..." --resolution "..." --source "agent work"
```

### Gather prior evidence

```bash
python toolkit.py evidence-brief --query "..."
```

### Generate a reusable skill draft

```bash
python toolkit.py skill-draft --name "some-workflow" --description "..." --step "..."
```

### Refresh an existing skill

```bash
python toolkit.py skill-refresh --skill-file ~/.openclaw/skills/some-skill/SKILL.md --lesson "..."
```

### Review/apply memory candidates

```bash
python toolkit.py recall-candidate --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### Validate before promotion

```bash
python scripts/validate_toolkit_outputs.py
```

This is enough to run the toolkit as a lightweight local memory + skill system even if you never use any agent-specific helper or wrapper.

---

## Command reference

### Memory and operations
- `toolkit.py memory-capture`
  - create daily + curated memory candidates
  - rejects secret-like text
  - rejects procedural/transient memory by default
- `toolkit.py decision-capture`
  - create a structured decision record (`what / why / how / outcome`)
- `toolkit.py incident-capture`
  - create a structured incident record (`symptoms / cause / resolution / related items`)
- `toolkit.py evidence-brief`
  - summarize related decisions, incidents, memory files, and skills before acting
- `toolkit.py recall-candidate`
  - preview curated memory candidates
  - optionally apply reviewed candidates into workspace memory files

### Skills
- `toolkit.py skill-draft`
  - generate a new local draft skill
- `toolkit.py skill-refresh`
  - generate a refreshed draft from an existing skill plus new lessons
- `toolkit.py skill-promote`
  - manually promote a reviewed draft into live skills

### Helpers
- `scripts/post_task_capture.py`
  - capture memory first, then optional skill draft
- `scripts/billy_pilot_capture.py`
  - example agent-specific wrapper over post-task capture
- `scripts/validate_toolkit_outputs.py`
  - check for obvious quality/safety problems before promotion
- `scripts/bootstrap_local_layout.py`
  - prepare local folders + example config files under `~/.openclaw/`

---

## Repo structure

```text
openclaw-agent-toolkit/
  modules/
    persistent-memory/
      README.md
      config.example.json
      prompts/
      scripts/
        memory_capture.py
        decision_capture.py
        incident_capture.py
        evidence_brief.py
        recall_candidate.py
    skill-autogen/
      README.md
      config.example.json
      prompts/
      scripts/
        generate_skill_draft.py
        refresh_skill_draft.py
        promote_skill_draft.py
  docs/
    AGENT_RULE_SNIPPETS.md
    BILLY_PILOT.md
    HERMES_AGENT_REVIEW.md
    SECURITY.md
    INSTALL.md
    INTEGRATION.md
    OPERATING_MODEL.md
    QUICKSTART.md
    QUALITY.md
    WORKFLOW.md
  scripts/
    billy_pilot_capture.py
    bootstrap_local_layout.py
    post_task_capture.py
    validate_toolkit_outputs.py
  toolkit.py
  .gitignore
```

---

## Security model

This repo is intentionally designed so that:
- no bot tokens
- no API keys
- no private credentials
- no machine-specific secrets
- no automatic outbound sync of sensitive memory

The toolkit only works with:
- local files
- local markdown summaries
- local draft outputs

Generated outputs should stay local by default.

---

## Important design rules

1. **Git repo is code + templates only**
   - no secrets
   - no personal memory files
   - no generated sensitive logs

2. **Generated outputs stay local by default**
   - local memory files
   - incident / decision outputs
   - draft skills
   - local config files

3. **Promotion is manual**
   - auto-generated skill drafts should not become live skills automatically

4. **OpenClaw updates should not break this toolkit**
   - integrations should rely on file workflows and light wrappers
   - avoid modifying installed OpenClaw package files

---

## Documentation map

See also:
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/INTEGRATION.md`
- `docs/WORKFLOW.md`
- `docs/QUALITY.md`
- `docs/BILLY_PILOT.md`
- `docs/AGENT_RULE_SNIPPETS.md`
- `docs/HERMES_AGENT_REVIEW.md`
- `docs/RECENT_UPDATES.md`
- `docs/SECURITY.md`

---

## Current recommendation

If you are adopting this toolkit today, the most practical starting set is:
- `memory-capture`
- `decision-capture`
- `incident-capture`
- `skill-draft`
- `skill-refresh`
- `evidence-brief`

That combination is enough to move from simple memory storage toward a **lightweight local operating memory system** for OpenClaw agents.
