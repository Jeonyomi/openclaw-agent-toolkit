# INSTALL

## Recommended approach

Clone this repo locally on each machine, then keep runtime state under `~/.openclaw/`.

The toolkit is meant to be:
- local-first
- machine-portable
- independent from OpenClaw package updates

---

## Example layout

```text
C:\Users\<USER>\repos\openclaw-agent-toolkit
C:\Users\<USER>\.openclaw\extensions\persistent-memory
C:\Users\<USER>\.openclaw\extensions\skill-autogen
C:\Users\<USER>\.openclaw\local-config\persistent-memory.local.json
C:\Users\<USER>\.openclaw\local-config\skill-autogen.local.json
C:\Users\<USER>\.openclaw\skills-drafts\
C:\Users\<USER>\.openclaw\skills\
C:\Users\<USER>\.openclaw\workspace\MEMORY.md
C:\Users\<USER>\.openclaw\workspace\memory\
```

---

## Install steps

### 1. Clone the repo

```bash
git clone <repo-url>
cd openclaw-agent-toolkit
```

### 2. Review security assumptions

Read:
- `docs/SECURITY.md`

### 3. Bootstrap local layout

```bash
python scripts/bootstrap_local_layout.py
```

### 4. Review generated local config files

Expected local config files:
- `~/.openclaw/local-config/persistent-memory.local.json`
- `~/.openclaw/local-config/skill-autogen.local.json`

### 5. Keep runtime outputs local

Do not commit generated runtime outputs.
Examples:
- `~/.openclaw/workspace/MEMORY.md`
- `~/.openclaw/workspace/memory/*.md`
- `~/.openclaw/skills-drafts/*`
- incident / decision outputs generated during use

### 6. Optional integration choices

Depending on your setup, you can:
- call `toolkit.py` directly from your repo checkout
- copy or symlink selected modules into `~/.openclaw/extensions/`
- copy generic snippets from `docs/AGENT_RULE_SNIPPETS.md` into your local agent instruction file

---

## Notes for other users

If you are setting this up for a different OpenClaw agent on another PC:
- reuse the same repo
- keep configs and outputs machine-local
- do not assume Billy-specific wording is required
- use the generic command set first:
  - `memory-capture`
  - `decision-capture`
  - `incident-capture`
  - `evidence-brief`
  - `skill-draft`
  - `skill-refresh`
  - `recall-candidate`

---

## Notes

- do not modify installed OpenClaw package files
- do not store secrets in this repo
- prefer machine-local config outside version control
- the bootstrap script only creates local folders and example config files if missing
- this repo should remain code + templates, not a dump of personal runtime memory
