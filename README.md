# openclaw-agent-toolkit

Reusable local toolkit for OpenClaw agents across multiple PCs.

## Goals

This repo is designed to provide **portable, update-independent agent enhancements** for OpenClaw, with a strong focus on:

1. **Persistent memory helpers**
2. **Automatic skill-draft generation after problem solving**

The design assumes:
- OpenClaw core should remain untouched
- The toolkit should live under `~/.openclaw/` or a separate workspace clone
- No secrets should be committed to git
- The same toolkit should be usable by Billy, Delly, or future agents on multiple PCs

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
- symlink or copy selected modules into `~/.openclaw/extensions/`
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
    OPERATING_MODEL.md
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

### Phase 3
- optional promotion workflow
- local review helpers
- quality filters and dedupe

## Status

This repo is currently a secure bootstrap skeleton for multi-PC OpenClaw agent enhancements.
