# WORKFLOW

## Goal

Define a practical way for OpenClaw agents to use this toolkit after meaningful work is completed.

## Recommended usage pattern

### 1. After a task is solved, decide if it produced durable value
Good candidates:
- decision worth remembering
- preference worth preserving
- project state update
- repeatable lesson
- repeatable workflow that could become a skill draft

### 2. Always capture memory first
Use:

```bash
python toolkit.py memory-capture --type decision --text "..." --source "..."
```

### 3. Only generate a skill draft when repetition value is clear
Use:

```bash
python toolkit.py skill-draft --name "..." --description "..." --step "..."
```

### 4. Promote only after review
Use:

```bash
python toolkit.py skill-promote --slug <slug>
```

## Practical shortcuts

### Generic post-task helper

```bash
python scripts/post_task_capture.py \
  --memory-type lesson \
  --memory-text "Service-based gateway restart is the safer default recovery path" \
  --source "OpenClaw recovery task" \
  --skill-name "openclaw-recovery" \
  --skill-description "Recovery workflow after install/update problems" \
  --skill-step "Check openclaw.json" \
  --skill-step "Restart gateway" \
  --skill-step "Verify both Telegram accounts"
```

### Billy pilot helper

```bash
python scripts/billy_pilot_capture.py \
  --kind decision \
  --text "Use service-based gateway restart as the default OpenClaw recovery path" \
  --source "Billy pilot"
```

## Agent operating guidance

### Billy-style usage
Best for:
- decisions
- preferences
- project state
- turning repeated ops patterns into draft skills

### Delly-style usage
Best for:
- implementation lessons
- repo-specific operational runbooks
- repeated deployment or recovery procedures

## Review rule
- memory capture can be frequent
- skill draft generation should be selective
- promotion should remain manual
