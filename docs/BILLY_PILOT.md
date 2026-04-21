# BILLY PILOT

## Pilot goal

Run a supervised pilot where Billy uses both:
- durable memory capture
- selective skill draft generation

The pilot should remain:
- local-only
- low-risk
- manually reviewed

## Recommended scope for Billy

### Use memory capture for
- decisions
- preferences
- project state
- durable lessons

### Use skill draft generation only when
- the workflow is clearly repeatable
- the procedure has at least a few concrete steps
- the draft would likely be reused later

## Do not use the pilot for
- secrets
- personal/private sensitive detail
- one-off noisy conversation fragments
- external/legal/financial statements that need stronger review

## Preferred command

```bash
python scripts/billy_pilot_capture.py \
  --kind decision \
  --text "Use service-based gateway restart as the default OpenClaw recovery path" \
  --source "Billy pilot" \
  --skill-name "openclaw-recovery" \
  --skill-description "Recovery workflow after install/update or broken gateway state" \
  --skill-step "Check openclaw.json" \
  --skill-step "Restart gateway" \
  --skill-step "Verify both Telegram accounts"
```

## Billy pilot rules

1. Capture memory first
2. Only add a skill draft when repetition value is clear
3. Review generated draft before promotion
4. Keep promotion manual
5. Run validation before promoting draft skills
6. Keep durable memory factual and long-lived; do not store transient progress logs or TODO state
7. Put reusable procedures and runbooks into skill drafts rather than memory

## Recommended operational loop for Billy

After meaningful work:

1. **If the outcome is a durable fact** → use `memory-capture`
2. **If the outcome is a repeatable workflow** → add `skill-draft` or `skill-refresh`
3. **If curated memory candidates have accumulated** → review with `recall-candidate` preview first, then `--apply`
4. **Before promoting any draft** → run validation

### Examples

Preview curated memory candidates:

```bash
python toolkit.py recall-candidate --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md
```

Apply curated memory candidates into workspace memory files:

```bash
python toolkit.py recall-candidate \
  --candidate-file modules/persistent-memory/output/curated-memory-candidate-YYYY-MM-DD.md \
  --memory-md ~/.openclaw/workspace/MEMORY.md \
  --daily-memory ~/.openclaw/workspace/memory/YYYY-MM-DD.md \
  --apply
```

Refresh an existing skill with a new lesson:

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/workspace/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

## Suggested pilot duration
- 1 to 2 weeks

## Success criteria
- Billy-generated memory entries are actually reusable
- Billy-generated drafts are selective rather than noisy
- at least a few pilot outputs are worth keeping/promoting

## Review command

```bash
python scripts/validate_toolkit_outputs.py
```

## Reuse on another PC

If another OpenClaw agent should follow the same pattern, use the generic snippets in:
- `docs/AGENT_RULE_SNIPPETS.md`

For non-Billy agents, prefer the generic toolkit rules rather than Billy-specific wording.
