from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PERSISTENT_MEMORY = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'memory_capture.py'
SKILL_DRAFT = ROOT / 'modules' / 'skill-autogen' / 'scripts' / 'generate_skill_draft.py'
PROMOTE_DRAFT = ROOT / 'modules' / 'skill-autogen' / 'scripts' / 'promote_skill_draft.py'


def run(args: list[str]) -> int:
    proc = subprocess.run([sys.executable, *args])
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description='Practical wrapper for openclaw-agent-toolkit MVP flows.')
    sub = parser.add_subparsers(dest='command', required=True)

    mem = sub.add_parser('memory-capture', help='Generate daily + curated memory draft outputs')
    mem.add_argument('--type', required=True, choices=['decision', 'preference', 'project-state', 'lesson'])
    mem.add_argument('--text', required=True)
    mem.add_argument('--source', default='')
    mem.add_argument('--output-dir', default='')

    draft = sub.add_parser('skill-draft', help='Generate a local draft SKILL.md')
    draft.add_argument('--name', required=True)
    draft.add_argument('--description', required=True)
    draft.add_argument('--trigger', action='append', default=[])
    draft.add_argument('--step', action='append', default=[])
    draft.add_argument('--caution', action='append', default=[])
    draft.add_argument('--output-dir', default='')

    promote = sub.add_parser('skill-promote', help='Promote a reviewed draft to live skills')
    promote.add_argument('--slug', required=True)
    promote.add_argument('--draft-root', default='')
    promote.add_argument('--live-root', default='')
    promote.add_argument('--copy', action='store_true')

    args = parser.parse_args()

    if args.command == 'memory-capture':
        cmd = [str(PERSISTENT_MEMORY), '--type', args.type, '--text', args.text]
        if args.source:
            cmd += ['--source', args.source]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        return run(cmd)

    if args.command == 'skill-draft':
        cmd = [str(SKILL_DRAFT), '--name', args.name, '--description', args.description]
        for v in args.trigger:
            cmd += ['--trigger', v]
        for v in args.step:
            cmd += ['--step', v]
        for v in args.caution:
            cmd += ['--caution', v]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        return run(cmd)

    if args.command == 'skill-promote':
        cmd = [str(PROMOTE_DRAFT), '--slug', args.slug]
        if args.draft_root:
            cmd += ['--draft-root', args.draft_root]
        if args.live_root:
            cmd += ['--live-root', args.live_root]
        if args.copy:
            cmd += ['--copy']
        return run(cmd)

    return 1


if __name__ == '__main__':
    raise SystemExit(main())
