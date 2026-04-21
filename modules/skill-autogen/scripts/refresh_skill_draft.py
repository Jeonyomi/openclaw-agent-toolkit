from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from generate_skill_draft import normalize_lines, slugify, build_skill_md, fingerprint, looks_secret


def parse_section_lines(text: str, heading: str) -> list[str]:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)", re.M)
    m = pattern.search(text)
    if not m:
        return []
    block = m.group(1)
    out = []
    for line in block.splitlines():
        line = line.strip()
        if re.match(r"^\d+\.\s+", line):
            out.append(re.sub(r"^\d+\.\s+", "", line).strip())
        elif line.startswith("- "):
            out.append(line[2:].strip())
    return normalize_lines(out)


def parse_frontmatter_field(text: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a refreshed draft from an existing live/draft skill plus new lessons.")
    parser.add_argument("--skill-file", required=True)
    parser.add_argument("--lesson", action="append", default=[])
    parser.add_argument("--trigger", action="append", default=[])
    parser.add_argument("--caution", action="append", default=[])
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--source", default="skill-refresh")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--allow-overwrite", action="store_true")
    args = parser.parse_args()

    skill_file = Path(args.skill_file)
    if not skill_file.exists():
        raise SystemExit(f"skill file not found: {skill_file}")

    raw = skill_file.read_text(encoding="utf-8")
    fields = [raw, args.source, *args.lesson, *args.trigger, *args.caution, *args.validation]
    if any(looks_secret(v) for v in fields):
        raise SystemExit("refusing to refresh skill draft because secret-like text was detected")

    name = parse_frontmatter_field(raw, "name") or skill_file.parent.name
    description = parse_frontmatter_field(raw, "description") or f"Refreshed draft for {name}"

    triggers = normalize_lines(parse_section_lines(raw, "When to use") + args.trigger)
    steps = normalize_lines(parse_section_lines(raw, "Steps") + args.lesson)
    cautions = normalize_lines(parse_section_lines(raw, "Cautions") + args.caution)
    validations = normalize_lines(parse_section_lines(raw, "Validation") + args.validation)

    if not validations:
        validations = ["Confirm the refreshed draft matches current real-world operating behavior"]

    refresh_name = f"{name}-refresh"
    slug = slugify(refresh_name)
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
        name=refresh_name,
        description=description,
        triggers=triggers,
        steps=steps,
        cautions=cautions,
        validations=validations,
        source=args.source,
    )
    skill_path.write_text(skill_md, encoding="utf-8")
    metadata = {
        "name": refresh_name,
        "slug": slug,
        "description": description,
        "triggers": triggers,
        "steps": steps,
        "cautions": cautions,
        "validations": validations,
        "source": args.source,
        "refreshedFrom": str(skill_file),
        "generatedAt": __import__('datetime').datetime.now().isoformat(),
        "status": "draft",
        "fingerprint": fp,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(skill_path))
    print(str(metadata_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
