from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

TOKEN_RE = re.compile(r"[\w가-힣]+", re.UNICODE)
STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "then", "what", "why", "how", "use", "using"}


def tokens(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_RE.findall(text or "") if len(t) > 1 and t.lower() not in STOP}


def score(query: set[str], text: str) -> float:
    doc = tokens(text)
    if not query or not doc:
        return 0.0
    return len(query & doc) / len(query)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def collect_files(root: Path, patterns: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for p in patterns:
        out.extend(root.glob(p))
    return [v for v in out if v.is_file()]


def top_hits(query_text: str, root: Path, patterns: Iterable[str], limit: int) -> list[dict]:
    q = tokens(query_text)
    hits = []
    for path in collect_files(root, patterns):
        text = read_text(path)
        s = score(q, text)
        if s <= 0:
            continue
        preview = re.sub(r"\s+", " ", text).strip()[:220]
        hits.append({"path": str(path), "score": round(s, 3), "preview": preview})
    hits.sort(key=lambda x: (-x["score"], x["path"]))
    return hits[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a lightweight evidence brief from local memory/skill/incident files.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    root = Path(args.root)
    output_root = root / "modules" / "persistent-memory" / "output"
    skills_root = Path.home() / ".openclaw" / "skills"
    draft_root = Path.home() / ".openclaw" / "skills-drafts"
    workspace_root = Path.home() / ".openclaw" / "workspace"

    result = {
        "query": args.query,
        "decisions": top_hits(args.query, output_root, ["decision-record-*.md"], args.limit),
        "incidents": top_hits(args.query, output_root / "incidents", ["incident-*.md"], args.limit),
        "memory": top_hits(args.query, workspace_root, ["MEMORY.md", "memory/*.md"], args.limit),
        "skills": top_hits(args.query, skills_root, ["*/SKILL.md"], args.limit),
        "skillDrafts": top_hits(args.query, draft_root, ["*/SKILL.md"], args.limit),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
