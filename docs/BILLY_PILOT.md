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

For Billy's local wrapper, prefer the workspace launcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\billy_post_task_capture.ps1 -Kind decision-structured -What "Use service-based gateway restart as the default OpenClaw recovery path" -Why "In-process restart can appear hung during drain/shutdown timeout" -How "Prefer service-based restart in docs and operator workflow" -Source "Billy pilot"
```

For repeatable workflow capture using the legacy memory+skill helper path:

```powershell
powershell -ExecutionPolicy Bypass -File .\billy_post_task_capture.ps1 -Kind lesson -Text "Service-based gateway restart is the safer default recovery path" -Source "Billy pilot" -SkillName "openclaw-recovery" -SkillDescription "Recovery workflow after install/update or broken gateway state" -SkillStep "Check openclaw.json" -SkillStep "Restart gateway" -SkillStep "Verify both Telegram accounts"
```

## Billy pilot rules

1. Capture memory first
2. Only add a skill draft when repetition value is clear
3. Review generated draft before promotion
4. Keep promotion manual
5. Run validation before promoting draft skills
6. Keep durable memory factual and long-lived; do not store transient progress logs or TODO state
7. Put reusable procedures and runbooks into skill drafts rather than memory

## Recommended operational loop

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

Capture an important operational decision:

```bash
python toolkit.py decision-capture \
  --what "Use service-based gateway restart as the default recovery path" \
  --why "In-process restart can appear hung during drain/shutdown timeout" \
  --how "Prefer service-based restart in docs and operator workflow"
```

Capture an incident after debugging/recovery work:

```bash
python toolkit.py incident-capture \
  --title "OpenClaw in-process restart looked hung" \
  --symptom "Gateway appeared stuck during shutdown" \
  --resolution "Use service-based gateway restart instead"
```

Gather prior evidence before risky work:

```bash
python toolkit.py evidence-brief --query "gateway restart recovery"
```

Refresh an existing skill with a new lesson:

```bash
python toolkit.py skill-refresh \
  --skill-file ~/.openclaw/workspace/skills/openclaw-recovery/SKILL.md \
  --lesson "Prefer service-based gateway restart as the default path unless a narrower recovery step is explicitly required"
```

## Minimum requirements for another PC

Updating this document alone is **not enough** to make another PC operational.
A second PC needs all of the following:

1. this repo cloned locally
2. local layout bootstrapped (`python scripts/bootstrap_local_layout.py`)
3. a local wrapper command or equivalent command sequence available on that machine
4. the agent's local instruction file updated with pilot rules
5. a real end-to-end validation run on that machine

### Practical apply checklist for another Billy-like PC

1. Clone or pull `openclaw-agent-toolkit`
2. Run:

```bash
python scripts/bootstrap_local_layout.py
```

3. Add the generic rules from `docs/AGENT_RULE_SNIPPETS.md` into the local agent instruction file
4. Add a local wrapper or command alias that the agent can call after meaningful work
5. Validate at least one real flow:
   - memory capture
   - curated candidate generation
   - reviewed apply into local `MEMORY.md` / `memory/YYYY-MM-DD.md`
6. Only after that should the PC be treated as pilot-operational

## Suggested pilot duration
- 1 to 2 weeks

## Success criteria
- agent-generated memory entries are actually reusable
- generated drafts are selective rather than noisy
- at least a few pilot outputs are worth keeping or promoting

## Review command

```bash
python scripts/validate_toolkit_outputs.py
```

## Reuse on another PC

If another OpenClaw agent should follow the same pattern, use the generic snippets in:
- `docs/AGENT_RULE_SNIPPETS.md`

For new setups, prefer the generic toolkit rules unless you intentionally want agent-specific wording.
