from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a reviewed local skill draft into a live skill directory.")
    parser.add_argument("--slug", required=True, help="Draft skill slug directory name")
    parser.add_argument("--draft-root", default=str(Path.home() / '.openclaw' / 'skills-drafts'))
    parser.add_argument("--live-root", default=str(Path.home() / '.openclaw' / 'skills'))
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    args = parser.parse_args()

    draft_root = Path(args.draft_root)
    live_root = Path(args.live_root)
    src = draft_root / args.slug
    dst = live_root / args.slug

    if not src.exists() or not src.is_dir():
        raise SystemExit(f"draft not found: {src}")

    skill_md = src / 'SKILL.md'
    if not skill_md.exists():
        raise SystemExit(f"draft missing SKILL.md: {skill_md}")

    live_root.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise SystemExit(f"target live skill already exists: {dst}")

    if args.copy:
        shutil.copytree(src, dst)
        print(f"copied: {src} -> {dst}")
    else:
        shutil.move(str(src), str(dst))
        print(f"moved: {src} -> {dst}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
