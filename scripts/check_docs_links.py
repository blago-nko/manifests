#!/usr/bin/env python3
"""Проверка внутренних ссылок документов экосистемы (INFRA-041)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = [ROOT / n for n in
        ["README.md", "AGENTS.md", "TASKS.md", "ROADMAP.md", "docs/STATUS.md"]]
LINK = re.compile(r"\[([^\]]+)\]\(([^)#]+\.md)\)")

bad = []
for doc in DOCS:
    if not doc.exists():
        continue
    for m in LINK.finditer(doc.read_text(encoding="utf-8")):
        target = (doc.parent / m.group(2)).resolve()
        if not target.exists():
            bad.append(f"{doc.name}: битая ссылка -> {m.group(2)}")

print("\n".join(bad) if bad else "links OK")
sys.exit(1 if bad else 0)
