# persistent-memory

Portable file-based helper module for durable memory capture across OpenClaw sessions.

## Scope
- generate memory candidate summaries
- append durable notes to daily memory draft files
- suggest curated long-term memory candidates

## Non-goals
- secret storage
- external sync
- opaque binary state

## Files
- `scripts/memory_capture.py` — local-safe CLI generator
- `prompts/durable_memory_rules.md` — guidance for what should be stored
- `output/` — local generated draft outputs (gitignored except `.gitkeep`)

## Example usage

```bash
python modules/persistent-memory/scripts/memory_capture.py \
  --type decision \
  --text "Prefer service-based openclaw gateway restart as default recovery path" \
  --source "OpenClaw recovery work"
```

Outputs:
- daily memory append candidate
- curated memory candidate
- jsonl-style manifest entry

## Safety
- secret-like strings are rejected
- output is local-only
- append-style generation only
- no automatic activation or sync

## Expected config
Use a machine-local config copied from `config.example.json`.
