# INSTALL

## Recommended approach

Clone this repo locally on each machine, then keep runtime state under `~/.openclaw/`.

## Example

```text
C:\Users\<USER>\repos\openclaw-agent-toolkit
C:\Users\<USER>\.openclaw\extensions\persistent-memory
C:\Users\<USER>\.openclaw\extensions\skill-autogen
```

## Install steps

1. Clone repo
2. Review `docs/SECURITY.md`
3. Copy or symlink desired module folders into `~/.openclaw/extensions/`
4. Create machine-local config files from `config.example.json`
5. Keep generated drafts and memory outputs local only

## Notes

- Do not modify OpenClaw installed package files
- Do not store secrets in this repo
- Prefer machine-local config outside version control
