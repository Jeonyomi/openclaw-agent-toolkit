# SECURITY

## Principles

This repo must remain safe to clone across multiple PCs.

### Never commit
- bot tokens
- API keys
- private keys
- personal memory files
- raw conversation exports
- `.openclaw/openclaw.json`
- local environment files

### Keep local only
- `memory/YYYY-MM-DD.md`
- `MEMORY.md`
- generated skill drafts containing project-private detail
- machine-local config files

## Safe operating model

- Repo contains only reusable templates, scripts, and docs
- Sensitive state lives outside the repo
- Default integration path is file-based and local-first
- Auto-generation should create drafts locally, not push anywhere

## Review rules

Before commit/push:
1. check `git status --short`
2. inspect diff for secrets
3. confirm no personal memory files are staged
4. confirm no machine-local configs are staged
