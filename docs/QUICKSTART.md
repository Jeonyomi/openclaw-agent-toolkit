# QUICKSTART

This guide shows the fastest useful path to running `openclaw-agent-toolkit` locally.

## 1. Bootstrap local layout

```bash
python scripts/bootstrap_local_layout.py
```

This prepares the basic local folder structure under `~/.openclaw/`.

---

## 2. Capture a durable memory

Use this when the outcome is a stable fact worth keeping.

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for OpenClaw recovery" \
  --source "OpenClaw recovery work"
```

---

## 3. Capture a structured decision

Use this when the important thing is **what was decided and why**.

```bash
python toolkit.py decision-capture \
  --what "Use service-based gateway restart as the default recovery path" \
  --why "In-process restart can appear hung during drain/shutdown timeout" \
  --how "Prefer service-based restart in docs and operator workflow"
```

---

## 4. Capture an incident

Use this when the important thing is **what went wrong and how it was fixed**.

```bash
python toolkit.py incident-capture \
  --title "OpenClaw in-process restart looked hung" \
  --symptom "Gateway appeared stuck during shutdown" \
  --resolution "Use service-based gateway restart instead"
```

---

## 5. Gather evidence before risky work

Use this before debugging, recovery, or repeated operational work.

```bash
python toolkit.py evidence-brief --query "gateway restart recovery"
```

---

## 6. Generate a draft skill

Use this when the result is a workflow worth reusing.

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

---

## 7. Refresh an existing skill draft from new lessons

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

---

## 8. Preview curated memory candidates

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

---

## 9. Apply curated memory candidates into workspace files

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

---

## 10. Validate outputs

```bash
python scripts/validate_toolkit_outputs.py
```

---

## 11. Promote a reviewed draft

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

---

## Notes

- outputs are local-only by default
- promotion is manual
- durable memory should stay factual and long-lived
- decisions should record `what / why / how`
- incidents should capture symptoms and resolution
- reusable procedures should usually become skills, not memory entries
- do not place secrets in text fields
