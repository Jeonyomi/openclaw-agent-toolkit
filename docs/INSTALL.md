# INSTALL

## Recommended approach

Clone this repo locally on each machine, then keep runtime state under `~/.openclaw/`.

## Example layout

```text
C:\Users\<USER>\repos\openclaw-agent-toolkit
C:\Users\<USER>\.openclaw\extensions\persistent-memory
C:\Users\<USER>\.openclaw\extensions\skill-autogen
C:\Users\<USER>\.openclaw\local-config\persistent-memory.local.json
C:\Users\<USER>\.openclaw\local-config\skill-autogen.local.json
C:\Users\<USER>\.openclaw\skills-drafts\
C:\Users\<USER>\.openclaw\skills\
```

## Install steps

1. Clone repo
2. Review `docs/SECURITY.md`
3. Run the local bootstrap helper:

```bash
python scripts/bootstrap_local_layout.py
```

4. Review generated local config files under:
- `~/.openclaw/local-config/persistent-memory.local.json`
- `~/.openclaw/local-config/skill-autogen.local.json`

5. Optionally copy or symlink selected modules into `~/.openclaw/extensions/`
6. Keep generated drafts and memory outputs local only

## Notes

- Do not modify OpenClaw installed package files
- Do not store secrets in this repo
- Prefer machine-local config outside version control
- The bootstrap script only creates local folders and example config files if missing
