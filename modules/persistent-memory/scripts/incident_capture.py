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
SEVERITIES = {"low", "medium", "high", "critical"}


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def slugify(text: str) -> str:
    text = normalize(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "incident"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a structured incident record as local markdown.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--symptom", action="append", default=[])
    parser.add_argument("--impact", default="")
    parser.add_argument("--cause", default="")
    parser.add_argument("--resolution", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--severity", default="medium", choices=sorted(SEVERITIES))
    parser.add_argument("--related-decision", action="append", default=[])
    parser.add_argument("--related-skill", action="append", default=[])
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "output" / "incidents"))
    parser.add_argument("--date", default=dt.datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    fields = [args.title, args.impact, args.cause, args.resolution, args.source, *args.symptom, *args.related_decision, *args.related_skill]
    if any(looks_secret(v or "") for v in fields):
        raise SystemExit("refusing to write incident output because secret-like text was detected")

    title = normalize(args.title)
    symptoms = [normalize(v) for v in args.symptom if normalize(v)]
    if not symptoms:
        raise SystemExit("at least one --symptom is required")
    impact = normalize(args.impact)
    cause = normalize(args.cause)
    resolution = normalize(args.resolution)
    source = normalize(args.source)
    related_decisions = [normalize(v) for v in args.related_decision if normalize(v)]
    related_skills = [normalize(v) for v in args.related_skill if normalize(v)]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"incident-{slugify(title)}-{args.date}.md"
    manifest = out_dir / f"incident-manifest-{args.date}.json"

    lines = [
        f"# Incident: {title}",
        "",
        f"- Date: {args.date}",
        f"- Severity: {args.severity}",
    ]
    if source:
        lines.append(f"- Source: {source}")
    lines.extend([
        "",
        "## Symptoms",
        *[f"- {v}" for v in symptoms],
    ])
    if impact:
        lines.extend(["", "## Impact", impact])
    if cause:
        lines.extend(["", "## Cause / Hypothesis", cause])
    if resolution:
        lines.extend(["", "## Resolution", resolution])
    if related_decisions or related_skills:
        lines.extend(["", "## Related"])
        lines.extend([f"- Decision: {v}" for v in related_decisions])
        lines.extend([f"- Skill: {v}" for v in related_skills])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = {
        "date": args.date,
        "title": title,
        "symptoms": symptoms,
        "impact": impact,
        "cause": cause,
        "resolution": resolution,
        "source": source,
        "severity": args.severity,
        "relatedDecisions": related_decisions,
        "relatedSkills": related_skills,
        "path": str(path),
        "generatedAt": dt.datetime.now().isoformat(),
    }
    with manifest.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
