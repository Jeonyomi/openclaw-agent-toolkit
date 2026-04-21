# INTEGRATION

## Intended model

This toolkit is designed to work alongside OpenClaw, not inside the OpenClaw package.

## Integration principles

- do not patch installed OpenClaw package files
- keep toolkit code in its own repo
- keep runtime state under `~/.openclaw/`
- keep generated outputs local-only

## Minimal practical usage

### 1. Capture a durable memory draft

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for recovery" \
  --source "OpenClaw recovery work"
```

### 2. Generate a new draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow after install/update issues" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

### 3. Refresh an existing skill when new lessons appear

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

### 4. Review curated memory candidates before long-term application

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### 5. Apply curated memory candidates after review

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

### 6. Promote after review

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

### 7. Use the post-task helper when both memory and draft capture are useful

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

## Recommended operating split

- **memory-capture** for durable facts
- **skill-draft / skill-refresh** for reusable procedures
- **recall-candidate** for reviewed promotion of curated memory candidates
- **validate_toolkit_outputs.py** before draft promotion

## Other-PC usage model

On another PC:
1. clone this repo
2. run `python scripts/bootstrap_local_layout.py`
3. review local config files
4. use `toolkit.py` or `scripts/post_task_capture.py` as needed
5. copy the generic integration rules from `docs/AGENT_RULE_SNIPPETS.md` into local agent instruction files if you want behavior-level integration

## Security note

Generated drafts and memory outputs should remain outside git and local to each machine.
