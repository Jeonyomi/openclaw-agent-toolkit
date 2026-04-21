# openclaw-agent-toolkit

Reusable local toolkit for OpenClaw agents across multiple PCs.

## What this repo does

This repo provides **portable, update-independent agent enhancements** for OpenClaw with a strong focus on:

1. **Durable memory capture**
2. **Draft skill generation and refresh**
3. **Manual promotion workflow for safe skill activation**
4. **Local-first operations that keep sensitive state out of git**

The intended design is:
- OpenClaw core remains untouched
- the toolkit lives in its own repo or under `~/.openclaw/`
- generated outputs stay local by default
- the same toolkit can be reused by Billy, Delly, or other agents on multiple PCs

## Current status

This repo now contains working local-safe flows for:
- durable memory draft capture
- curated memory candidate review/apply flow
- draft skill generation
- existing skill refresh draft generation
- manual draft promotion
- validation and lightweight quality checks
- Billy pilot helper and generic agent rule snippets
- local bootstrap/install flow for other PCs

## Core idea: memory vs skill vs recall

This toolkit now follows a Hermes-inspired split:

- **Memory** = durable facts worth keeping across sessions
  - decisions
  - preferences
  - stable project state
  - repeatable lessons
- **Skill** = reusable procedure or runbook
  - recovery workflows
  - repo workflows
  - scheduler/deployment checklists
  - operational playbooks
- **Recall / review** = candidate promotion step
  - review curated memory candidates before applying them to long-term workspace memory

That means:
- transient progress logs should **not** go into durable memory
- TODOs/blockers should **not** go into durable memory
- reusable procedures should usually become **skill drafts**, not memory entries

## Quick start

### 1. Bootstrap local layout

```bash
python scripts/bootstrap_local_layout.py
```

### 2. Capture durable memory

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for OpenClaw recovery" \
  --source "OpenClaw recovery work"
```

### 3. Generate a draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

### 4. Refresh an existing skill with new lessons

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

### 5. Preview curated memory candidates

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### 6. Apply curated memory candidates into workspace memory files

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

### 7. Validate local outputs before promotion

```bash
python scripts/validate_toolkit_outputs.py
```

### 8. Promote a reviewed draft skill

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

### 9. Billy pilot helper

```bash
python scripts/billy_pilot_capture.py \
  --kind decision \
  --text "Use service-based gateway restart" \
  --source "Billy pilot"
```

## Recommended usage flow after meaningful work

After a meaningful task is completed:

1. **If the outcome is a durable fact** → use `memory-capture`
2. **If the outcome is a repeatable workflow** → use `skill-draft` or `skill-refresh`
3. **If curated memory candidates have accumulated** → review with `recall-candidate`, then `--apply`
4. **Before promoting draft skills** → run validation
5. **Promotion stays manual**

## For other people / another PC

If you want to use this repo on another PC or with another OpenClaw agent:

### Setup steps

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

6. Copy the generic agent snippets from:
- `docs/AGENT_RULE_SNIPPETS.md`

into your local agent instructions if you want behavior-level integration.

### Minimal usage pattern

For a generic OpenClaw agent on another machine:

```bash
python toolkit.py memory-capture --type decision --text "..." --source "agent pilot"
```

```bash
python toolkit.py skill-draft --name "some-workflow" --description "..." --step "..."
```

```bash
python toolkit.py skill-refresh --skill-file ~/.openclaw/skills/some-skill/SKILL.md --lesson "..."
```

```bash
python toolkit.py recall-candidate --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

```bash
python scripts/validate_toolkit_outputs.py
```

## Command reference

### Memory flows
- `toolkit.py memory-capture`
  - create daily + curated memory candidates
  - rejects secret-like text
  - now rejects procedural/transient memory by default
- `toolkit.py recall-candidate`
  - preview curated memory candidates
  - optionally apply reviewed candidates into workspace memory files

### Skill flows
- `toolkit.py skill-draft`
  - generate a new local draft skill
- `toolkit.py skill-refresh`
  - generate a refreshed draft from an existing skill + new lessons
- `toolkit.py skill-promote`
  - manually promote a reviewed draft into live skills

### Helpers
- `scripts/post_task_capture.py`
  - capture memory first, then optional skill draft
- `scripts/billy_pilot_capture.py`
  - Billy-friendly wrapper over post-task capture
- `scripts/validate_toolkit_outputs.py`
  - check for obvious quality/safety problems before promotion
- `scripts/bootstrap_local_layout.py`
  - prepare local folders + example config files under `~/.openclaw/`

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

## Recommended install layout

Suggested layout:

```text
~/.openclaw/
  extensions/
    persistent-memory/
    skill-autogen/
  local-config/
    persistent-memory.local.json
    skill-autogen.local.json
  skills-drafts/
  skills/
  workspace/
    MEMORY.md
    memory/
```

## Important design rules

1. **Git repo is code + templates only**
   - no secrets
   - no personal memory files
   - no generated sensitive logs

2. **Generated outputs stay local by default**
   - `memory/YYYY-MM-DD.md`
   - `skills-drafts/*`
   - local config files

3. **Promotion is manual**
   - auto-generated skill drafts should not become live skills automatically

4. **OpenClaw updates should not break this toolkit**
   - integrations should rely on file workflows and light wrappers
   - avoid modifying installed OpenClaw package files

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

## Recent updates

Recent improvements added in the Hermes-inspired upgrade pass:
- stricter separation between durable memory and procedural skills
- `recall-candidate` for curated memory review/apply
- `skill-refresh` for evolving live skills via new lessons
- richer skill draft structure with validation + maintenance notes
- stronger validation for imperative/transient memory and malformed draft steps
- clearer Billy operating loop and reusable agent snippets for other PCs
