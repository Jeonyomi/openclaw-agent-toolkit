from __future__ import annotations

import argparse
import datetime as dt
import hashlib
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


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled-skill"


def _split_compound(value: str) -> list[str]:
    value = re.sub(r"\s+", " ", value).strip()
    if not value:
        return []
    if "," in value and not re.search(r"https?://", value):
        parts = [v.strip() for v in value.split(",") if v.strip()]
        if len(parts) > 1:
            return parts
    return [value]


def normalize_lines(values: list[str]) -> list[str]:
    out: list[str] = []
    for v in values:
        for piece in _split_compound(v):
            s = re.sub(r"\s+", " ", piece).strip(" -")
            if s and s not in out:
                out.append(s)
    return out


def ensure_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text.endswith((".", "!", "?")):
        return text
    return text + "."


def build_skill_md(
    name: str,
    description: str,
    triggers: list[str],
    steps: list[str],
    cautions: list[str],
    validations: list[str],
    source: str,
) -> str:
    frontmatter = [
        "---",
        f"name: {name}",
        f"description: {description}",
        "status: draft",
        f"generated_at: {dt.datetime.now().isoformat()}",
    ]
    if triggers:
        frontmatter.append("triggers:")
        frontmatter.extend([f"  - {t}" for t in triggers])
    if source:
        frontmatter.append(f"source: {source}")
    frontmatter.append("---")

    lines = [
        *frontmatter,
        "",
        f"# {name}",
        "",
        "## When to use",
    ]
    if triggers:
        lines.extend([f"- {ensure_sentence(t)}" for t in triggers])
    else:
        lines.append("- Use when the same operational pattern is likely to recur.")

    lines.extend([
        "",
        "## Steps",
    ])
    if steps:
        lines.extend([f"{idx+1}. {ensure_sentence(step)}" for idx, step in enumerate(steps)])
    else:
        lines.append("1. Review the recurring workflow and apply it carefully.")

    lines.extend([
        "",
        "## Validation",
    ])
    if validations:
        lines.extend([f"- {ensure_sentence(v)}" for v in validations])
    else:
        lines.append("- Confirm the workflow actually solved the problem before promoting this draft.")

    lines.extend([
        "",
        "## Cautions",
    ])
    if cautions:
        lines.extend([f"- {ensure_sentence(c)}" for c in cautions])
    else:
        lines.append("- Review for secrets or machine-specific details before promoting this draft.")

    lines.extend([
        "",
        "## Status",
        "- Draft only. Manual review required before promotion to a live skill.",
        "",
        "## Maintenance notes",
        "- If future runs reveal missing steps, patch the draft before promotion.",
    ])
    return "\n".join(lines) + "\n"


def fingerprint(description: str, steps: list[str], triggers: list[str], cautions: list[str], validations: list[str]) -> str:
    payload = json.dumps(
        {
            "description": description,
            "steps": steps,
            "triggers": triggers,
            "cautions": cautions,
            "validations": validations,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local-only draft SKILL.md from solved-problem notes.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--trigger", action="append", default=[])
    parser.add_argument("--step", action="append", default=[])
    parser.add_argument("--caution", action="append", default=[])
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--source", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--allow-overwrite", action="store_true")
    args = parser.parse_args()

    raw_fields = [args.name, args.description, args.source, *args.trigger, *args.step, *args.caution, *args.validation]
    if any(looks_secret(v) for v in raw_fields):
        raise SystemExit("refusing to generate skill draft because secret-like text was detected")

    name = args.name.strip()
    description = re.sub(r"\s+", " ", args.description).strip()
    source = re.sub(r"\s+", " ", args.source).strip()
    triggers = normalize_lines(args.trigger)
    steps = normalize_lines(args.step)
    cautions = normalize_lines(args.caution)
    validations = normalize_lines(args.validation)

    slug = slugify(name)
    base = Path(args.output_dir) if args.output_dir else Path.home() / ".openclaw" / "skills-drafts"
    target_dir = base / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    fp = fingerprint(description, steps, triggers, cautions, validations)
    skill_path = target_dir / "SKILL.md"
    metadata_path = target_dir / "draft-metadata.json"

    if metadata_path.exists() and not args.allow_overwrite:
        try:
            old = json.loads(metadata_path.read_text(encoding="utf-8"))
            if old.get("fingerprint") == fp:
                print(f"duplicate-draft-skip: {metadata_path}")
                return 0
        except Exception:
            pass

    skill_md = build_skill_md(
        name=name,
        description=description,
        triggers=triggers,
        steps=steps,
        cautions=cautions,
        validations=validations,
        source=source,
    )
    skill_path.write_text(skill_md, encoding="utf-8")
    metadata = {
        "name": name,
        "slug": slug,
        "description": description,
        "triggers": triggers,
        "steps": steps,
        "cautions": cautions,
        "validations": validations,
        "source": source,
        "generatedAt": dt.datetime.now().isoformat(),
        "status": "draft",
        "fingerprint": fp,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(skill_path))
    print(str(metadata_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
