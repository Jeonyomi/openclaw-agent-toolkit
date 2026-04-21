# openclaw-agent-toolkit

Reusable local toolkit for OpenClaw agents across multiple PCs.

## Goals

This repo is designed to provide **portable, update-independent agent enhancements** for OpenClaw, with a strong focus on:

1. **Persistent memory helpers**
2. **Automatic skill-draft generation after problem solving**
3. **Manual promotion workflow for safe skill activation**

The design assumes:
- OpenClaw core should remain untouched
- The toolkit should live under `~/.openclaw/` or a separate workspace clone
- No secrets should be committed to git
- The same toolkit should be usable by Billy, Delly, or future agents on multiple PCs

## Quick start

### 1. Bootstrap local layout
```bash
python scripts/bootstrap_local_layout.py
```

### 2. Capture durable memory
```bash
python toolkit.py memory-capture --type decision --text "Prefer service-based gateway restart" --source "OpenClaw recovery"
```

### 3. Generate a draft skill
```bash
python toolkit.py skill-draft --name "openclaw-recovery" --description "Recovery workflow for Billy/Delly" --step "Check openclaw.json" --step "Restart gateway"
```

### 4. Promote a reviewed draft
```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

See also:
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/INTEGRATION.md`

## Current modules

### 1. persistent-memory
Purpose:
- help record durable memories after sessions/tasks
- separate raw daily memory from curated long-term memory
- keep memory operations file-based and portable

### 2. skill-autogen
Purpose:
- generate draft `SKILL.md` files after repeated or high-value problem solving
- create draft-only outputs first
- require manual promotion before activating skills

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

On each machine:

- clone this repo anywhere convenient
- keep runtime state under `~/.openclaw/`
- keep machine-local config outside git

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
    skill-autogen/
      README.md
      config.example.json
      prompts/
      scripts/
  docs/
    SECURITY.md
    INSTALL.md
    INTEGRATION.md
    OPERATING_MODEL.md
    QUICKSTART.md
  scripts/
    bootstrap_local_layout.py
  toolkit.py
  .gitignore
```

## Roadmap

### Phase 1
- portable repo skeleton
- security baseline
- install model
- module boundaries

### Phase 2
- persistent memory helper implementation
- skill draft generator implementation
- manual promotion helper
- practical wrapper flow
- local bootstrap/install flow

### Phase 3
- local review helpers
- quality filters and dedupe
- optional wrappers/hooks for practical OpenClaw workflows

## Status

This repo now contains working local-safe MVPs for:
- persistent memory draft capture
- skill draft generation
- manual skill draft promotion
- simple wrapper-based usage flow
- local multi-PC bootstrap/install flow
