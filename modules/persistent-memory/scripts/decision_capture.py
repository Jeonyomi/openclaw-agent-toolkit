from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?:api[_-]?key|token|secret|private[_-]?key)\s*[:=]\s*\S+", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def append_unique_block(path: Path, block: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if re.sub(r"\s+", " ", block).strip() in re.sub(r"\s+", " ", existing).strip():
        return False
    with path.open("a", encoding="utf-8") as f:
        f.write(block + "\n\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a structured decision record as local markdown.")
    parser.add_argument("--what", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--how", required=True)
    parser.add_argument("--outcome", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--related-skill", action="append", default=[])
    parser.add_argument("--related-project", action="append", default=[])
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "output"))
    parser.add_argument("--date", default=dt.datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    fields = [args.what, args.why, args.how, args.outcome, args.source, *args.tag, *args.related_skill, *args.related_project]
    if any(looks_secret(v or "") for v in fields):
        raise SystemExit("refusing to write decision output because secret-like text was detected")

    what = normalize(args.what)
    why = normalize(args.why)
    how = normalize(args.how)
    outcome = normalize(args.outcome)
    source = normalize(args.source)
    tags = [normalize(v) for v in args.tag if normalize(v)]
    related_skills = [normalize(v) for v in args.related_skill if normalize(v)]
    related_projects = [normalize(v) for v in args.related_project if normalize(v)]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"decision-record-{args.date}.md"
    manifest = out_dir / f"decision-manifest-{args.date}.json"

    lines = [
        "## Decision",
        f"- What: {what}",
        f"- Why: {why}",
        f"- How: {how}",
    ]
    if outcome:
        lines.append(f"- Outcome: {outcome}")
    if source:
        lines.append(f"- Source: {source}")
    if tags:
        lines.append(f"- Tags: {', '.join(tags)}")
    if related_skills:
        lines.append(f"- Related skills: {', '.join(related_skills)}")
    if related_projects:
        lines.append(f"- Related projects: {', '.join(related_projects)}")

    block = "\n".join(lines)
    written = append_unique_block(path, block)

    payload = {
        "date": args.date,
        "what": what,
        "why": why,
        "how": how,
        "outcome": outcome,
        "source": source,
        "tags": tags,
        "relatedSkills": related_skills,
        "relatedProjects": related_projects,
        "written": written,
        "generatedAt": dt.datetime.now().isoformat(),
    }
    with manifest.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
