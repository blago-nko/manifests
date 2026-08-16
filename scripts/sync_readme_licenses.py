#!/usr/bin/env python3
"""SAM-LIC-010: синхронизация README + раскатка readme-license-check.
Запуск: только из GitHub Codespaces. Создаёт ветку и PR в каждом репо."""
import subprocess, tempfile, os, re, sys, json

ORG = "blago-nko"
BRANCH = "fix/sam-lic-010-readme-sync"
DRY = "--dry-run" in sys.argv

WEB_SECTION = """## 📜 Лицензирование

Этот проект использует модель двойного лицензирования согласно ЛИЦ.md (SAM-LIC-010):

### GNU Affero General Public License v3.0

Весь программный код, включая:

- HTML/CSS/JS шаблоны
- Конфигурации Hugo/Next.js
- CI/CD скрипты (`.github/workflows/*`)
- Сборочные скрипты

Лицензирован под **GNU Affero General Public License v3.0** (см. файл `LICENSE`).

### CC BY-NC 4.0

Смысловой контент, включая:

- Тексты статей и публикаций (`content/`)
- Биографии, новости, образовательные материалы
- Изображения авторского контента

Лицензирован под **CC BY-NC 4.0** (см. файл `LICENSE-CONTENT`).
"""

MANIFESTS_SECTION = """## ⚖️ Двойное Лицензирование

- **Исходный код** (скрипты, Next.js, Astro, шаблоны Hugo) — **GNU Affero General Public License v3.0** (см. `LICENSE`)
- **Контент, тексты, архитектурные манифесты и БД** — **CC BY-NC 4.0** (см. `LICENSE-CONTENT`)

Подробности: ЛИЦ.md
"""

CHECK_WF = """name: readme-license-check
on:
  push:
    branches: [main]
  pull_request:
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: README не должен содержать устаревшие лицензии
        run: |
          if grep -nE 'MIT License|CC BY-SA' README.md; then
            echo "::error::README.md содержит устаревшие лицензии (MIT/CC BY-SA). Актуально: AGPLv3 + CC BY-NC 4.0 (SAM-LIC-010)."
            exit 1
          fi
"""

RE_WEB = re.compile(r"^## 📜 Лицензирование\n.*?(?=^#\s|^\*\s\*\s\*|^---|\Z)", re.S | re.M)
RE_MAN = re.compile(r"^## ⚖️ Двойное Лицензирование\n.*?(?=^##\s|\Z)", re.S | re.M)
RE_STALE = re.compile(r"MIT License|CC BY-SA|CC BY 4\.0")

def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[fail] cmd: {' '.join(cmd)}")
        print(f"[fail] stdout: {p.stdout.strip()}")
        print(f"[fail] stderr: {p.stderr.strip()}")
        raise SystemExit(p.returncode)
    return p

repos = json.loads(run(["gh", "repo", "list", ORG, "--limit", "100",
                        "--json", "nameWithOwner"]).stdout)

for r in repos:
    slug = r["nameWithOwner"]
    with tempfile.TemporaryDirectory() as td:
        dst = os.path.join(td, "repo")
        run(["gh", "repo", "clone", slug, dst, "--", "--depth", "50"])
        changed = False

        readme = os.path.join(dst, "README.md")
        if os.path.exists(readme):
            txt = open(readme, encoding="utf-8").read()
            if RE_STALE.search(txt):
                if "## 📜 Лицензирование" in txt:
                    txt = RE_WEB.sub(WEB_SECTION, txt, count=1)
                elif "## ⚖️ Двойное Лицензирование" in txt:
                    txt = RE_MAN.sub(MANIFESTS_SECTION, txt, count=1)
                open(readme, "w", encoding="utf-8").write(txt)
                changed = True

        wf_dir = os.path.join(dst, ".github", "workflows")
        wf = os.path.join(wf_dir, "readme-license-check.yml")
        if not os.path.exists(wf):
            os.makedirs(wf_dir, exist_ok=True)
            open(wf, "w", encoding="utf-8").write(CHECK_WF)
            changed = True

        if not changed:
            print(f"[skip] {slug}: уже консистентен")
            continue
        if DRY:
            print(f"[dry ] {slug}: будет изменён")
            continue

        run(["git", "checkout", "-b", BRANCH], dst)
        run(["git", "add", "-A"], dst)
        staged = run(["git", "status", "--porcelain"], dst).stdout.strip()
        if not staged:
            print(f"[skip] {slug}: нет изменений для коммита")
            continue
        run(["git", "commit", "-m",
             "fix(LIC): SAM-LIC-010 — README → AGPLv3 + CC BY-NC 4.0 + readme-license-check"], dst)
        run(["git", "push", "-u", "origin", BRANCH], dst)
        run(["gh", "pr", "create", "--repo", slug, "--base", "main", "--head", BRANCH,
             "--title", "fix(LIC): SAM-LIC-010 — синхронизация README и CI-проверка лицензий",
             "--body", "Автоматическая синхронизация с manifests (SAM-LIC-010). Основание: SAM-EXC-001."], dst)
        print(f"[pr  ] {slug}: PR создан")