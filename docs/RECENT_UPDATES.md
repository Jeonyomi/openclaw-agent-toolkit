# RECENT UPDATES

## Hermes-inspired upgrade pass

The toolkit was upgraded to better separate:
- durable memory
- reusable skills
- reviewed memory promotion

### Added
- `toolkit.py recall-candidate`
- `toolkit.py skill-refresh`
- `docs/HERMES_AGENT_REVIEW.md`
- stronger Billy operating loop guidance
- clearer reusable snippets for other PCs/agents

### Improved
- `memory-capture`
  - now rejects procedural/transient memory by default
  - better aligns durable memory with factual long-lived notes
- `skill-draft`
  - richer structure with `When to use`, `Steps`, `Validation`, `Cautions`, `Maintenance notes`
- `validate_toolkit_outputs.py`
  - checks imperative memory
  - checks transient/progress-style memory
  - checks missing skill sections
  - checks malformed comma-joined steps

### Result
The toolkit is now better suited for:
- Billy-style post-task memory capture
- repeatable workflow drafting
- safer long-term memory curation
- reuse on other PCs with less ambiguity
