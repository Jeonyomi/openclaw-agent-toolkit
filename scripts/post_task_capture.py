from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLKIT = ROOT / 'toolkit.py'


def run(cmd: list[str]) -> int:
    return subprocess.run([sys.executable, *cmd]).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description='Post-task helper for memory and optional skill-draft capture.')
    parser.add_argument('--memory-type', required=True, choices=['decision', 'preference', 'project-state', 'lesson'])
    parser.add_argument('--memory-text', required=True)
    parser.add_argument('--source', default='post-task-capture')
    parser.add_argument('--skill-name', default='')
    parser.add_argument('--skill-description', default='')
    parser.add_argument('--skill-trigger', action='append', default=[])
    parser.add_argument('--skill-step', action='append', default=[])
    parser.add_argument('--skill-caution', action='append', default=[])
    parser.add_argument('--memory-output-dir', default='')
    parser.add_argument('--skill-output-dir', default='')
    args = parser.parse_args()

    code = run([
        str(TOOLKIT),
        'memory-capture',
        '--type', args.memory_type,
        '--text', args.memory_text,
        '--source', args.source,
        *( ['--output-dir', args.memory_output_dir] if args.memory_output_dir else [] ),
    ])
    if code != 0:
        return code

    if args.skill_name and args.skill_description:
        code = run([
            str(TOOLKIT),
            'skill-draft',
            '--name', args.skill_name,
            '--description', args.skill_description,
            *sum([['--trigger', v] for v in args.skill_trigger], []),
            *sum([['--step', v] for v in args.skill_step], []),
            *sum([['--caution', v] for v in args.skill_caution], []),
            *( ['--output-dir', args.skill_output_dir] if args.skill_output_dir else [] ),
        ])
        return code

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
