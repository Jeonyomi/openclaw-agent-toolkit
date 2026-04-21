from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?:api[_-]?key|token|secret|private[_-]?key)\s*[:=]\s*\S+", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]
HEADER_RE = re.compile(r"^##\s+(Decision candidate|Preference candidate|Project-state candidate|Lesson candidate)\s*$", re.M)


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def infer_type(block: str) -> str:
    m = HEADER_RE.search(block)
    if not m:
        return "lesson"
    label = m.group(1).lower()
    if label.startswith("decision"):
        return "decision"
    if label.startswith("preference"):
        return "preference"
    if label.startswith("project-state"):
        return "project-state"
    return "lesson"


def parse_blocks(text: str) -> list[dict]:
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n(?=## )", text) if b.strip()]
    out: list[dict] = []
    for block in raw_blocks:
        if not block.startswith("## "):
            continue
        entry_type = infer_type(block)
        fact = ""
        source = ""
        review = ""
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- "):
                body = line[2:].strip()
                if body.lower().startswith("source:"):
                    source = normalize(body.split(":", 1)[1])
                elif body.lower().startswith("review warnings:"):
                    review = normalize(body.split(":", 1)[1])
                elif not fact:
                    fact = normalize(body)
        if fact:
            out.append({
                "type": entry_type,
                "text": fact,
                "source": source,
                "review": review,
                "raw": block,
            })
    return out


def append_unique_section(path: Path, heading: str, bullet: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if bullet in existing:
        return False
    content = existing.rstrip()
    if not content:
        new_text = f"# MEMORY.md\n\n## {heading}\n- {bullet}\n"
    else:
        section_pat = re.compile(rf"(^##\s+{re.escape(heading)}\s*$)", re.M)
        if section_pat.search(content):
            new_text = re.sub(
                rf"(^##\s+{re.escape(heading)}\s*$)",
                rf"\1\n- {bullet}",
                content,
                count=1,
                flags=re.M,
            )
        else:
            new_text = content + f"\n\n## {heading}\n- {bullet}\n"
    path.write_text(new_text if new_text.endswith("\n") else new_text + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote curated memory candidates into workspace memory files.")
    parser.add_argument("--candidate-file", required=True)
    parser.add_argument("--memory-md", default="")
    parser.add_argument("--daily-memory", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    candidate_file = Path(args.candidate_file)
    if not candidate_file.exists():
        raise SystemExit(f"candidate file not found: {candidate_file}")

    text = candidate_file.read_text(encoding="utf-8")
    if looks_secret(text):
        raise SystemExit("refusing to process candidate file because secret-like text was detected")

    entries = parse_blocks(text)[: max(1, args.limit)]
    if not entries:
        raise SystemExit("no candidate entries found")

    memory_md = Path(args.memory_md) if args.memory_md else Path.home() / ".openclaw" / "workspace" / "MEMORY.md"
    daily_memory = Path(args.daily_memory) if args.daily_memory else Path.home() / ".openclaw" / "workspace" / "memory" / f"{dt.datetime.now().strftime('%Y-%m-%d')}.md"

    preview = {
        "candidateFile": str(candidate_file),
        "memoryMd": str(memory_md),
        "dailyMemory": str(daily_memory),
        "apply": args.apply,
        "entries": entries,
    }

    if not args.apply:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    memory_md.parent.mkdir(parents=True, exist_ok=True)
    daily_memory.parent.mkdir(parents=True, exist_ok=True)

    applied = []
    for entry in entries:
        heading = {
            "decision": "Decisions",
            "preference": "Preferences",
            "project-state": "Project State",
            "lesson": "Lessons",
        }[entry["type"]]
        bullet = entry["text"]
        if entry.get("source"):
            bullet += f" (source: {entry['source']})"
        memory_written = append_unique_section(memory_md, heading, bullet)
        daily_line = f"- Promoted memory candidate ({entry['type']}): {entry['text']}"
        existing_daily = daily_memory.read_text(encoding='utf-8') if daily_memory.exists() else ""
        daily_written = False
        if daily_line not in existing_daily:
            with daily_memory.open("a", encoding="utf-8") as f:
                f.write(daily_line + "\n")
            daily_written = True
        applied.append({
            "type": entry["type"],
            "text": entry["text"],
            "memoryWritten": memory_written,
            "dailyWritten": daily_written,
        })

    print(json.dumps({
        "success": True,
        "candidateFile": str(candidate_file),
        "memoryMd": str(memory_md),
        "dailyMemory": str(daily_memory),
        "applied": applied,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
