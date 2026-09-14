#!/usr/bin/env python3
"""Автогенерация секций README.md: дерево файлов, репозитории организации, статус."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
ORG = "blago-nko"

BLOCKS = {
    "TREE": ("<!-- README:TREE:BEGIN -->", "<!-- README:TREE:END -->"),
    "REPOS": ("<!-- README:REPOS:BEGIN -->", "<!-- README:REPOS:END -->"),
    "STATUS": ("<!-- README:STATUS:BEGIN -->", "<!-- README:STATUS:END -->"),
}

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
EXCLUDE_FILES = {"FETCH_HEAD", "AGENTS.md.backup", "temp.md"}


def build_tree(base: Path) -> list[str]:
    lines: list[str] = []
    items = sorted(
        (p for p in base.iterdir()
         if p.name not in EXCLUDE_DIRS and p.name not in EXCLUDE_FILES),
        key=lambda p: (p.is_file(), p.name.lower()),
    )
    for p in items:
        if p.is_dir():
            lines.append(f"- 📁 **{p.name}/**")
            lines.extend("  " + s for s in build_tree(p))
        else:
            rel = p.relative_to(ROOT).as_posix()
            lines.append(f"- [{p.name}]({rel})")
    return lines


def fetch_repos() -> list[dict] | None:
    try:
        proc = subprocess.run(
            ["gh", "api", f"orgs/{ORG}/repos?per_page=100",
             "-q", '.[] | [.name, (.description // ""), .html_url] | @tsv'],
            capture_output=True, check=True, timeout=60,
        )
    except Exception as exc:
        print(f"⚠️ Репозитории организации недоступны: {exc}")
        return None
    repos = []
    for line in proc.stdout.decode("utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            repos.append({"name": parts[0], "desc": parts[1] or "—", "url": parts[2]})
    return sorted(repos, key=lambda r: r["name"])


def replace_block(text: str, begin: str, end: str, body: str) -> str:
    if begin not in text or end not in text:
        return text
    pre, rest = text.split(begin, 1)
    _, post = rest.split(end, 1)
    return pre + begin + "\n\n" + body + "\n\n" + end + post


def main() -> None:
    text = README.read_text(encoding="utf-8")

    b, e = BLOCKS["TREE"]
    text = replace_block(text, b, e, "\n".join(build_tree(ROOT)))

    repos = fetch_repos()
    if repos is not None:
        b, e = BLOCKS["REPOS"]
        text = replace_block(text, b, e, "\n".join(
            f"- [{r['name']}]({r['url']}) — {r['desc']}" for r in repos))

    b, e = BLOCKS["STATUS"]
    text = replace_block(text, b, e,
        "**Текущий статус экосистемы:** [docs/STATUS.md](docs/STATUS.md)\n\n"
        "Файл обновляется автоматически workflow `update-status.yml`.")

    README.write_text(text, encoding="utf-8")
    print("✅ README.md: автосекции обновлены")


if __name__ == "__main__":
    main()
