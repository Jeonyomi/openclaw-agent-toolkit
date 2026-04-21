from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

ALLOWED_TYPES = {"decision", "preference", "project-state", "lesson"}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?:api[_-]?key|token|secret|private[_-]?key)\s*[:=]\s*\S+", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]
PROCEDURAL_PATTERNS = [
    re.compile(r"^(always|never|do |don't |run |use |check |restart |verify |update |create |delete |patch)\b", re.I),
    re.compile(r"\b(step|workflow|procedure|runbook|playbook|checklist)\b", re.I),
]
TRANSIENT_PATTERNS = [
    re.compile(r"\b(todo|next step|follow up|follow-up|wip|in progress|blocked|temporary|for now)\b", re.I),
    re.compile(r"\b(pass|failed|failing|fixed|completed|done)\b", re.I),
]


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def looks_procedural(text: str) -> bool:
    return any(p.search(text) for p in PROCEDURAL_PATTERNS)


def looks_transient(text: str) -> bool:
    return any(p.search(text) for p in TRANSIENT_PATTERNS)


def memory_style_warnings(entry_type: str, text: str) -> list[str]:
    warnings: list[str] = []
    if looks_procedural(text):
        warnings.append("looks procedural; workflows should usually become skill drafts, not memory")
    if looks_transient(text) and entry_type != "project-state":
        warnings.append("looks transient or progress-log-like; session/task state should usually stay out of durable memory")
    if len(text) < 12:
        warnings.append("very short memory text may be too vague to be durable")
    return warnings


def render_daily(entry_type: str, text: str, source: str | None, warnings: list[str]) -> str:
    label = {
        "decision": "Decision",
        "preference": "Preference",
        "project-state": "Project state",
        "lesson": "Lesson",
    }[entry_type]
    suffix = f" (source: {source})" if source else ""
    line = f"- {label}: {text}{suffix}"
    if warnings:
        line += f" [warnings: {'; '.join(warnings)}]"
    return line


def render_curated(entry_type: str, text: str, source: str | None, warnings: list[str]) -> str:
    title = {
        "decision": "Decision candidate",
        "preference": "Preference candidate",
        "project-state": "Project-state candidate",
        "lesson": "Lesson candidate",
    }[entry_type]
    lines = [f"## {title}", f"- {text}"]
    if source:
        lines.append(f"- Source: {source}")
    if warnings:
        lines.append(f"- Review warnings: {'; '.join(warnings)}")
    return "\n".join(lines)


def append_unique_line(path: Path, line: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = [v.strip() for v in existing.splitlines() if v.strip()]
    if line.strip() in lines:
        return False
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return True


def append_unique_block(path: Path, block: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    normalized_existing = re.sub(r"\s+", " ", existing).strip()
    normalized_block = re.sub(r"\s+", " ", block).strip()
    if normalized_block and normalized_block in normalized_existing:
        return False
    with path.open("a", encoding="utf-8") as f:
        f.write(block + "\n\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local-safe durable memory draft outputs.")
    parser.add_argument("--type", required=True, choices=sorted(ALLOWED_TYPES))
    parser.add_argument("--text", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "output"))
    parser.add_argument("--date", default=dt.datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--allow-procedural", action="store_true")
    parser.add_argument("--allow-transient", action="store_true")
    args = parser.parse_args()

    text = normalize(args.text)
    source = normalize(args.source)

    if not text:
        raise SystemExit("text is empty after normalization")
    if looks_secret(text) or (source and looks_secret(source)):
        raise SystemExit("refusing to write output because secret-like text was detected")

    warnings = memory_style_warnings(args.type, text)
    if not args.allow_procedural and any("procedural" in w for w in warnings):
        raise SystemExit("refusing to write output because the text looks procedural; capture it as a skill draft or pass --allow-procedural")
    if not args.allow_transient and any("transient" in w for w in warnings):
        raise SystemExit("refusing to write output because the text looks transient/progress-like; revise it as a durable fact or pass --allow-transient")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    daily_path = out_dir / f"daily-memory-entry-{args.date}.md"
    curated_path = out_dir / f"curated-memory-candidate-{args.date}.md"
    manifest_path = out_dir / f"capture-manifest-{args.date}.json"

    daily_entry = render_daily(args.type, text, source or None, warnings)
    curated_entry = render_curated(args.type, text, source or None, warnings)

    daily_written = append_unique_line(daily_path, daily_entry)
    curated_written = append_unique_block(curated_path, curated_entry)

    manifest = {
        "date": args.date,
        "entryType": args.type,
        "text": text,
        "source": source,
        "warnings": warnings,
        "dailyOutput": str(daily_path),
        "curatedOutput": str(curated_path),
        "dailyWritten": daily_written,
        "curatedWritten": curated_written,
        "generatedAt": dt.datetime.now().isoformat(),
    }
    with manifest_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(manifest, ensure_ascii=False) + "\n")

    print(str(daily_path))
    print(str(curated_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
