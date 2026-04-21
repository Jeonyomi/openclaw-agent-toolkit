# QUICKSTART

## 1. Capture durable memory

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for OpenClaw recovery" \
  --source "OpenClaw recovery work"
```

## 2. Generate a draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

## 3. Promote a reviewed draft

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

## Notes
- outputs are local-only by default
- promotion is manual
- do not place secrets in text fields
