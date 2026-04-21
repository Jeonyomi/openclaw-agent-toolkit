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

### 2. Generate a draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow after install/update issues" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

### 3. Promote after review

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

## Other-PC usage model

On another PC:
1. clone this repo
2. run `python scripts/bootstrap_local_layout.py`
3. review local config files
4. use `toolkit.py` commands as needed

## Security note

Generated drafts and memory outputs should remain outside git and local to each machine.
