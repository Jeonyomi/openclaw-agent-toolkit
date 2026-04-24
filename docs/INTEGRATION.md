# INTEGRATION

## Intended model

This toolkit is designed to work **alongside OpenClaw**, not inside the installed OpenClaw package.

## Integration principles

- do not patch installed OpenClaw package files
- keep toolkit code in its own repo
- keep runtime state under `~/.openclaw/`
- keep generated outputs local-only
- prefer lightweight file workflows over deep framework coupling

---

## Practical integration model

The toolkit fits into agent operation at four points:

1. **after meaningful work** -> capture memory / decision / incident
2. **when a workflow is repeatable** -> generate or refresh a skill draft
3. **before risky work** -> gather prior evidence
4. **before long-term promotion** -> review and validate

---

## Minimal practical usage

### Capture a durable memory draft

```bash
python toolkit.py memory-capture \
  --type decision \
  --text "Prefer service-based gateway restart for recovery" \
  --source "OpenClaw recovery work"
```

### Capture a structured decision

```bash
python toolkit.py decision-capture \
  --what "Use service-based gateway restart as the default recovery path" \
  --why "In-process restart can appear hung during drain/shutdown timeout" \
  --how "Prefer service-based restart in docs and operator workflow"
```

### Capture a structured incident

```bash
python toolkit.py incident-capture \
  --title "OpenClaw in-process restart looked hung" \
  --symptom "Gateway appeared stuck during shutdown" \
  --resolution "Use service-based gateway restart instead"
```

### Gather prior evidence

```bash
python toolkit.py evidence-brief --query "gateway restart recovery"
```

### Generate a new draft skill

```bash
python toolkit.py skill-draft \
  --name "openclaw-recovery" \
  --description "Recovery workflow after install/update issues" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts"
```

### Refresh an existing skill when new lessons appear

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

### Review curated memory candidates before long-term application

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

### Apply curated memory candidates after review

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

### Promote after review

```bash
python toolkit.py skill-promote --slug openclaw-recovery
```

---

## Recommended operating split

- **memory-capture** for durable facts
- **decision-capture** for important choices with rationale
- **incident-capture** for failures, outages, and repeated mistakes
- **evidence-brief** before risky debugging/recovery work
- **skill-draft / skill-refresh** for reusable procedures
- **recall-candidate** for reviewed promotion of curated memory candidates
- **validate_toolkit_outputs.py** before draft promotion

---

## Other-PC usage model

On another PC:
1. clone this repo
2. run `python scripts/bootstrap_local_layout.py`
3. review local config files
4. use `toolkit.py` commands directly as needed
5. copy the generic integration rules from `docs/AGENT_RULE_SNIPPETS.md` into local agent instruction files if you want behavior-level integration

This works even if the other agent is not Billy.

---

## Security note

Generated drafts, incidents, decisions, and memory outputs should remain outside git and local to each machine.
