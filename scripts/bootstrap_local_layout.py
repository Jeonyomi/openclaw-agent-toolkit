from __future__ import annotations

import argparse
import json
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Bootstrap local OpenClaw toolkit layout under ~/.openclaw')
    parser.add_argument('--openclaw-home', default=str(Path.home() / '.openclaw'))
    args = parser.parse_args()

    root = Path(args.openclaw_home)
    extensions = root / 'extensions'
    local_config = root / 'local-config'
    skills_drafts = root / 'skills-drafts'
    skills_live = root / 'skills'
    memory_dir = root / 'workspace' / 'memory'

    for p in [extensions, local_config, skills_drafts, skills_live, memory_dir]:
        ensure_dir(p)

    persistent_cfg = {
        'workspaceMemoryDir': str(memory_dir).replace('\\', '/'),
        'longTermMemoryFile': str((root / 'workspace' / 'MEMORY.md')).replace('\\', '/'),
        'captureRules': {
            'storeDecisions': True,
            'storePreferences': True,
            'storeProjectState': True,
            'storeSecrets': False,
        },
    }
    skill_cfg = {
        'draftOutputDir': str(skills_drafts).replace('\\', '/'),
        'minStepsForDraft': 3,
        'requireManualPromotion': True,
        'filters': {
            'allowRepeatedOps': True,
            'allowRecoveryPatterns': True,
            'allowProjectSpecificDrafts': True,
            'excludeSecrets': True,
        },
    }

    write_if_missing(local_config / 'persistent-memory.local.json', json.dumps(persistent_cfg, ensure_ascii=False, indent=2))
    write_if_missing(local_config / 'skill-autogen.local.json', json.dumps(skill_cfg, ensure_ascii=False, indent=2))

    print(str(root))
    print(str(local_config / 'persistent-memory.local.json'))
    print(str(local_config / 'skill-autogen.local.json'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
