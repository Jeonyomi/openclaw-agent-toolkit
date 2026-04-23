from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PERSISTENT_MEMORY = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'memory_capture.py'
DECISION_CAPTURE = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'decision_capture.py'
INCIDENT_CAPTURE = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'incident_capture.py'
EVIDENCE_BRIEF = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'evidence_brief.py'
RECALL_CANDIDATE = ROOT / 'modules' / 'persistent-memory' / 'scripts' / 'recall_candidate.py'
SKILL_DRAFT = ROOT / 'modules' / 'skill-autogen' / 'scripts' / 'generate_skill_draft.py'
REFRESH_DRAFT = ROOT / 'modules' / 'skill-autogen' / 'scripts' / 'refresh_skill_draft.py'
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
    mem.add_argument('--allow-procedural', action='store_true')
    mem.add_argument('--allow-transient', action='store_true')

    decision = sub.add_parser('decision-capture', help='Capture a structured decision record')
    decision.add_argument('--what', required=True)
    decision.add_argument('--why', required=True)
    decision.add_argument('--how', required=True)
    decision.add_argument('--outcome', default='')
    decision.add_argument('--source', default='')
    decision.add_argument('--tag', action='append', default=[])
    decision.add_argument('--related-skill', action='append', default=[])
    decision.add_argument('--related-project', action='append', default=[])
    decision.add_argument('--output-dir', default='')

    incident = sub.add_parser('incident-capture', help='Capture a structured incident record')
    incident.add_argument('--title', required=True)
    incident.add_argument('--symptom', action='append', default=[])
    incident.add_argument('--impact', default='')
    incident.add_argument('--cause', default='')
    incident.add_argument('--resolution', default='')
    incident.add_argument('--source', default='')
    incident.add_argument('--severity', default='medium', choices=['low', 'medium', 'high', 'critical'])
    incident.add_argument('--related-decision', action='append', default=[])
    incident.add_argument('--related-skill', action='append', default=[])
    incident.add_argument('--output-dir', default='')

    evidence = sub.add_parser('evidence-brief', help='Summarize related decisions/incidents/memory/skills before acting')
    evidence.add_argument('--query', required=True)
    evidence.add_argument('--root', default='')
    evidence.add_argument('--limit', type=int, default=5)

    recall = sub.add_parser('recall-candidate', help='Promote curated memory candidates into workspace memory files')
    recall.add_argument('--candidate-file', required=True)
    recall.add_argument('--memory-md', default='')
    recall.add_argument('--daily-memory', default='')
    recall.add_argument('--apply', action='store_true')
    recall.add_argument('--limit', type=int, default=10)

    draft = sub.add_parser('skill-draft', help='Generate a local draft SKILL.md')
    draft.add_argument('--name', required=True)
    draft.add_argument('--description', required=True)
    draft.add_argument('--trigger', action='append', default=[])
    draft.add_argument('--step', action='append', default=[])
    draft.add_argument('--caution', action='append', default=[])
    draft.add_argument('--validation', action='append', default=[])
    draft.add_argument('--source', default='')
    draft.add_argument('--output-dir', default='')

    refresh = sub.add_parser('skill-refresh', help='Generate a refreshed draft from an existing skill plus new lessons')
    refresh.add_argument('--skill-file', required=True)
    refresh.add_argument('--lesson', action='append', default=[])
    refresh.add_argument('--trigger', action='append', default=[])
    refresh.add_argument('--caution', action='append', default=[])
    refresh.add_argument('--validation', action='append', default=[])
    refresh.add_argument('--source', default='skill-refresh')
    refresh.add_argument('--output-dir', default='')
    refresh.add_argument('--allow-overwrite', action='store_true')

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
        if args.allow_procedural:
            cmd += ['--allow-procedural']
        if args.allow_transient:
            cmd += ['--allow-transient']
        return run(cmd)

    if args.command == 'decision-capture':
        cmd = [str(DECISION_CAPTURE), '--what', args.what, '--why', args.why, '--how', args.how]
        if args.outcome:
            cmd += ['--outcome', args.outcome]
        if args.source:
            cmd += ['--source', args.source]
        for v in args.tag:
            cmd += ['--tag', v]
        for v in args.related_skill:
            cmd += ['--related-skill', v]
        for v in args.related_project:
            cmd += ['--related-project', v]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        return run(cmd)

    if args.command == 'incident-capture':
        cmd = [str(INCIDENT_CAPTURE), '--title', args.title, '--severity', args.severity]
        for v in args.symptom:
            cmd += ['--symptom', v]
        if args.impact:
            cmd += ['--impact', args.impact]
        if args.cause:
            cmd += ['--cause', args.cause]
        if args.resolution:
            cmd += ['--resolution', args.resolution]
        if args.source:
            cmd += ['--source', args.source]
        for v in args.related_decision:
            cmd += ['--related-decision', v]
        for v in args.related_skill:
            cmd += ['--related-skill', v]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        return run(cmd)

    if args.command == 'evidence-brief':
        cmd = [str(EVIDENCE_BRIEF), '--query', args.query, '--limit', str(args.limit)]
        if args.root:
            cmd += ['--root', args.root]
        return run(cmd)

    if args.command == 'recall-candidate':
        cmd = [str(RECALL_CANDIDATE), '--candidate-file', args.candidate_file, '--limit', str(args.limit)]
        if args.memory_md:
            cmd += ['--memory-md', args.memory_md]
        if args.daily_memory:
            cmd += ['--daily-memory', args.daily_memory]
        if args.apply:
            cmd += ['--apply']
        return run(cmd)

    if args.command == 'skill-draft':
        cmd = [str(SKILL_DRAFT), '--name', args.name, '--description', args.description]
        for v in args.trigger:
            cmd += ['--trigger', v]
        for v in args.step:
            cmd += ['--step', v]
        for v in args.caution:
            cmd += ['--caution', v]
        for v in args.validation:
            cmd += ['--validation', v]
        if args.source:
            cmd += ['--source', args.source]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        return run(cmd)

    if args.command == 'skill-refresh':
        cmd = [str(REFRESH_DRAFT), '--skill-file', args.skill_file, '--source', args.source]
        for v in args.lesson:
            cmd += ['--lesson', v]
        for v in args.trigger:
            cmd += ['--trigger', v]
        for v in args.caution:
            cmd += ['--caution', v]
        for v in args.validation:
            cmd += ['--validation', v]
        if args.output_dir:
            cmd += ['--output-dir', args.output_dir]
        if args.allow_overwrite:
            cmd += ['--allow-overwrite']
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
