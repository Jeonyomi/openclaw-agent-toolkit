# skill-autogen

Portable helper module for generating local skill drafts after repeated or high-value problem solving.

## Scope
- create draft-only `SKILL.md` files
- keep outputs local
- support later manual promotion

## Non-goals
- automatic live skill activation
- automatic publishing
- broad uncontrolled skill generation

## Files
- `scripts/generate_skill_draft.py` — local draft generator CLI
- `scripts/promote_skill_draft.py` — manual promotion helper
- `prompts/draft_skill_rules.md` — guidance for what should become a draft skill

## Example: generate a draft

```bash
python modules/skill-autogen/scripts/generate_skill_draft.py \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install or update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts" \
  --caution "Remove machine-specific details before promotion"
```

Default draft output location:
- `~/.openclaw/skills-drafts/<slug>/SKILL.md`
- `~/.openclaw/skills-drafts/<slug>/draft-metadata.json`

## Deduplication
- identical draft description + steps generate the same fingerprint
- repeated generation of the same draft is skipped by default
- use `--allow-overwrite` if you intentionally want to refresh an existing draft

## Example: promote a reviewed draft

```bash
python modules/skill-autogen/scripts/promote_skill_draft.py --slug openclaw-recovery
```

This moves the draft from:
- `~/.openclaw/skills-drafts/openclaw-recovery`

to:
- `~/.openclaw/skills/openclaw-recovery`

Use `--copy` if you want to keep the original draft in place while testing.

## Safety
- local-only output
- draft status only until explicitly promoted
- secret-like strings are rejected during draft generation
- promotion is manual by design

## Expected config
Use a machine-local config copied from `config.example.json`.
