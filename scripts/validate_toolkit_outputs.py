from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?:api[_-]?key|token|secret|private[_-]?key)\s*[:=]\s*\S+", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]


def has_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def validate_skill_drafts(root: Path) -> list[str]:
    issues: list[str] = []
    if not root.exists():
        return issues
    for skill_md in root.rglob('SKILL.md'):
        text = skill_md.read_text(encoding='utf-8', errors='ignore')
        if has_secret(text):
            issues.append(f'secret-like text in {skill_md}')
        if 'Draft only. Manual review required' not in text:
            issues.append(f'missing draft status note in {skill_md}')
        metadata = skill_md.parent / 'draft-metadata.json'
        if not metadata.exists():
            issues.append(f'missing metadata next to {skill_md}')
        else:
            try:
                data = json.loads(metadata.read_text(encoding='utf-8'))
                if not data.get('fingerprint'):
                    issues.append(f'missing fingerprint in {metadata}')
            except Exception as e:
                issues.append(f'invalid json in {metadata}: {e}')
    return issues


def validate_memory_outputs(root: Path) -> list[str]:
    issues: list[str] = []
    if not root.exists():
        return issues
    for path in root.rglob('*.md'):
        text = path.read_text(encoding='utf-8', errors='ignore')
        if has_secret(text):
            issues.append(f'secret-like text in {path}')
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate local toolkit outputs for basic quality/safety issues.')
    parser.add_argument('--skill-drafts-root', default=str(Path.home() / '.openclaw' / 'skills-drafts'))
    parser.add_argument('--memory-output-root', default=str(Path.home() / '.openclaw' / 'workspace' / 'memory'))
    args = parser.parse_args()

    issues = []
    issues.extend(validate_skill_drafts(Path(args.skill_drafts_root)))
    issues.extend(validate_memory_outputs(Path(args.memory_output_root)))

    if issues:
        for issue in issues:
            print(issue)
        return 1

    print('validation-ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
