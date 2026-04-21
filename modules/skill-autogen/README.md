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
- `prompts/draft_skill_rules.md` — guidance for what should become a draft skill

## Example usage

```bash
python modules/skill-autogen/scripts/generate_skill_draft.py \
  --name "openclaw-recovery" \
  --description "Recovery workflow for Billy/Delly after reinstall or broken gateway state" \
  --trigger "Use when Billy or Delly stops responding after install/update" \
  --step "Check openclaw.json" \
  --step "Restart gateway" \
  --step "Verify both Telegram accounts" \
  --caution "Remove machine-specific secrets before promotion"
```

Default output location:
- `~/.openclaw/skills-drafts/<slug>/SKILL.md`
- `~/.openclaw/skills-drafts/<slug>/draft-metadata.json`

## Safety
- local-only output
- draft status only
- secret-like strings are rejected
- no automatic activation

## Expected config
Use a machine-local config copied from `config.example.json`.
