#!/usr/bin/env python3
"""PROC-001: автовалидация реестра TASKS.md.

Правила: у каждой задачи непустой статус; у закрытых (✅) непустой результат;
ID уникальны (дубли строк запрещены).
"""
import collections
import re
import sys
from pathlib import Path

bad = []
ids = collections.Counter()
first = {}
for n, line in enumerate(Path("TASKS.md").read_text(encoding="utf-8").split("\n"), 1):
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.split("|")]
    if len(cells) < 8:
        continue
    tid = cells[1].replace("**", "")
    if not re.fullmatch(r"[A-Z]+-\d+", tid):
        continue
    ids[tid] += 1
    first.setdefault(tid, n)
    status, comment = cells[6], cells[7]
    if not status:
        bad.append(f"{tid} (строка {n}): пустой статус")
    if status == "✅" and not comment:
        bad.append(f"{tid} (строка {n}): закрыта без результата")
for tid, c in ids.items():
    if c > 1:
        bad.append(f"{tid}: строк в реестре = {c} (первая на строке {first[tid]})")

print("\n".join(bad) if bad else "tasks registry OK")
sys.exit(1 if bad else 0)
