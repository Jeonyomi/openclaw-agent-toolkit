# QUALITY

## Goals

Add lightweight safeguards so toolkit outputs stay usable and low-noise.

## Current safeguards

### Skill draft dedupe
- identical draft description + steps produce the same fingerprint
- repeated generation of the same draft is skipped by default
- use `--allow-overwrite` only when you intentionally want to refresh a draft

### Output validation
Use:

```bash
python scripts/validate_toolkit_outputs.py
```

Checks include:
- secret-like text in draft skills
- secret-like text in memory markdown outputs
- missing `draft-metadata.json`
- missing draft fingerprint
- missing draft status note in `SKILL.md`

## Practical recommendation
- run validation before promoting draft skills
- keep generation frequent enough to be useful, but selective enough to avoid noise
