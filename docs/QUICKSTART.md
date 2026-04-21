# QUICKSTART

## 1. Bootstrap local layout

```bash
python scripts/bootstrap_local_layout.py
```

## 2. Capture durable memory

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for OpenClaw recovery" \
  --source "OpenClaw recovery work"
```

## 3. Generate a draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

## 4. Refresh an existing skill draft from new lessons

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

## 5. Preview curated memory candidates

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

## 6. Apply curated memory candidates into workspace files

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

## 7. Validate outputs

```bash
python scripts/validate_toolkit_outputs.py
```

## 8. Promote a reviewed draft

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

## Notes
- outputs are local-only by default
- promotion is manual
- durable memory should stay factual and long-lived
- reusable procedures should usually become skills, not memory entries
- do not place secrets in text fields
