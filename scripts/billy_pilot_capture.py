from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST_TASK = ROOT / 'scripts' / 'post_task_capture.py'


def main() -> int:
    parser = argparse.ArgumentParser(description='Billy pilot helper for memory + optional skill capture.')
    parser.add_argument('--kind', required=True, choices=['decision', 'preference', 'project-state', 'lesson'])
    parser.add_argument('--text', required=True)
    parser.add_argument('--source', default='Billy pilot')
    parser.add_argument('--skill-name', default='')
    parser.add_argument('--skill-description', default='')
    parser.add_argument('--skill-step', action='append', default=[])
    parser.add_argument('--skill-trigger', action='append', default=[])
    parser.add_argument('--skill-caution', action='append', default=[])
    parser.add_argument('--memory-output-dir', default='')
    parser.add_argument('--skill-output-dir', default='')
    args = parser.parse_args()

    cmd = [
        sys.executable,
        str(POST_TASK),
        '--memory-type', args.kind,
        '--memory-text', args.text,
        '--source', args.source,
    ]

    if args.skill_name and args.skill_description:
        cmd += ['--skill-name', args.skill_name, '--skill-description', args.skill_description]
        for v in args.skill_trigger:
            cmd += ['--skill-trigger', v]
        for v in args.skill_step:
            cmd += ['--skill-step', v]
        for v in args.skill_caution:
            cmd += ['--skill-caution', v]
    if args.memory_output_dir:
        cmd += ['--memory-output-dir', args.memory_output_dir]
    if args.skill_output_dir:
        cmd += ['--skill-output-dir', args.skill_output_dir]

    return subprocess.run(cmd).returncode


if __name__ == '__main__':
    raise SystemExit(main())
