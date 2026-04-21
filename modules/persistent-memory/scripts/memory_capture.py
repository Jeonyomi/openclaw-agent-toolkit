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


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_daily(entry_type: str, text: str, source: str | None) -> str:
    label = {
        "decision": "Decision",
        "preference": "Preference",
        "project-state": "Project state",
        "lesson": "Lesson",
    }[entry_type]
    suffix = f" (source: {source})" if source else ""
    return f"- {label}: {text}{suffix}"


def render_curated(entry_type: str, text: str, source: str | None) -> str:
    title = {
        "decision": "Decision candidate",
        "preference": "Preference candidate",
        "project-state": "Project-state candidate",
        "lesson": "Lesson candidate",
    }[entry_type]
    lines = [f"## {title}", f"- {text}"]
    if source:
        lines.append(f"- Source: {source}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local-safe durable memory draft outputs.")
    parser.add_argument("--type", required=True, choices=sorted(ALLOWED_TYPES))
    parser.add_argument("--text", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "output"))
    parser.add_argument("--date", default=dt.datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    text = normalize(args.text)
    source = normalize(args.source)

    if not text:
        raise SystemExit("text is empty after normalization")
    if looks_secret(text) or (source and looks_secret(source)):
        raise SystemExit("refusing to write output because secret-like text was detected")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    daily_path = out_dir / f"daily-memory-entry-{args.date}.md"
    curated_path = out_dir / f"curated-memory-candidate-{args.date}.md"
    manifest_path = out_dir / f"capture-manifest-{args.date}.json"

    daily_entry = render_daily(args.type, text, source or None)
    curated_entry = render_curated(args.type, text, source or None)

    with daily_path.open("a", encoding="utf-8") as f:
        f.write(daily_entry + "\n")

    with curated_path.open("a", encoding="utf-8") as f:
        f.write(curated_entry + "\n\n")

    manifest = {
        "date": args.date,
        "entryType": args.type,
        "text": text,
        "source": source,
        "dailyOutput": str(daily_path),
        "curatedOutput": str(curated_path),
        "generatedAt": dt.datetime.now().isoformat(),
    }
    with manifest_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(manifest, ensure_ascii=False) + "\n")

    print(str(daily_path))
    print(str(curated_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
