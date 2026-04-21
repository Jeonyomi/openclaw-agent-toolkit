# AGENT RULE SNIPPETS

Use these snippets to integrate the toolkit into an OpenClaw agent's default operating rules on another PC.

## Purpose

These snippets are designed to be copied into local agent-facing files such as:
- `AGENTS.md`
- `WORKFLOW_AUTO.md`
- other local operational instructions

They are intentionally generic so they can be reused by Billy, Gurugent, or other future agents.

---

## Snippet A — Toolkit pilot rule (generic)

```md
## Agent Toolkit Pilot (mandatory for meaningful completed work)
The `openclaw-agent-toolkit` pilot is active.

When a meaningful task is completed, the agent should normally do both of the following unless the content is too sensitive, too trivial, or too noisy:
- capture durable memory
- generate a draft skill when the workflow is clearly repeatable

### Good candidates
- operating decisions
- user preferences
- project state changes
- repeatable recovery / repo / scheduler / deployment procedures
- lessons learned worth preserving

### Do NOT capture
- secrets / keys / tokens
- raw sensitive internal details
- one-off trivial chatter
- low-confidence legal / financial / personal-private content

### Default behavior
- capture memory first
- add a skill draft only when repetition value is clear
- keep promotion manual
- if uncertain, skip skill draft and keep only memory capture
```

---

## Snippet B — Generic post-task command usage

```md
### Toolkit usage after meaningful work
Use the local toolkit wrapper after meaningful completed work.

Examples:

```bash
python toolkit.py memory-capture --type decision --text "..." --source "agent pilot"
```

```bash
python scripts/post_task_capture.py --memory-type lesson --memory-text "..." --source "agent pilot"
```
```

---

## Snippet C — Startup / restart checklist addition

```md
## Toolkit reminder
If the agent toolkit pilot is active, use the toolkit after meaningful completed work unless the result is too sensitive, too trivial, or too noisy.
```
