#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys, subprocess, os

BRANCH = "fix/architecture-consistency-2026-08-13"
COMMIT_MSG = """fix(manifests): архитектурная консистентность

Протоколы: SAM-INFRA-011/012/013, SAM-LIC-007/008, SAM-MIG-005
- ЛИЦ: CC BY-SA -> CC BY в заголовке; CC BY-NC-ND для витрины САН
- САМ: ноу-хау -> copyright; Yandex Object Storage; почтовый шлюз webmaster (fallback)
- СУМКа: пометка активации webmaster после миграции
- МИГРАЦИЯ: изоляция статического архива САН на Vercel (can-secure-dev)
"""

PATCHES = [
  {"file":"ЛИЦ.md","type":"lit","required":True,
   "old":"Лицензирование и интеллектуальная собственность (CC BY-SA 4.0 + MIT)",
   "new":"Лицензирование и интеллектуальная собственность (CC BY 4.0 + MIT)",
   "desc":"ЛИЦ заголовок: CC BY-SA -> CC BY (SAM-INFRA-011)"},
  {"file":"ЛИЦ.md","type":"lit","required":True,
   "old":"сопровождается лицензией CC BY 4.0 с атрибуцией источника (карточки САН).",
   "new":"сопровождается лицензией **CC BY-NC-ND 4.0** (NonCommercial, NoDerivatives) с атрибуцией источника (карточки САН), чтобы защитить базу от коммерческого парсинга агрегаторами.",
   "desc":"ЛИЦ: защита витрины САН -> CC BY-NC-ND (SAM-LIC-008)"},
  {"file":"САМ.md","type":"lit","required":True,
   "old":"Регистрация алгоритмов, БД, тематических паспортов как ноу-хау.",
   "new":"Регистрация прав на составные базы данных и алгоритмы (Copyright). Ноу-хау применяется только к закрытым промптам и весам локальных ИИ-моделей.",
   "desc":"САМ 1.14: ноу-хау -> copyright (SAM-LIC-007)"},
  {"file":"САМ.md","type":"lit","required":True,
   "old":"Warm (MinIO/S3 — история цен, сырые парсинги),",
   "new":"Warm (Yandex Object Storage для Parquet/DuckDB Knowledge Graph; MinIO/R2 для истории цен),",
   "desc":"САМ 4.9: унификация S3-хранилищ (SAM-INFRA-012)"},
  {"file":"САМ.md","type":"regex","required":True,
   "old":r'(\|\s*Контактный адрес на всех 14 сайтах\s*\|\s*)`?blagorussia@yandex\.ru`?(\s*\|)',
   "new":r'\1`webmaster@blagorussia.ru` ⚠️ До завершения Миграционного Этапа 1 fallback: `blagorussia@yandex.ru`\2',
   "desc":"САМ В2: контактный email -> webmaster + fallback (SAM-INFRA-013)"},
  {"file":"САМ.md","type":"regex","required":True,
   "old":r'(\|\s*Техническая поддержка\s*\|\s*)`?blagorussia@yandex\.ru`?(\s*\|)',
   "new":r'\1`webmaster@blagorussia.ru` ⚠️ До завершения Миграционного Этапа 1 fallback: `blagorussia@yandex.ru`\2',
   "desc":"САМ В2: техподдержка email -> webmaster + fallback (SAM-INFRA-013)"},
  {"file":"САМ.md","type":"regex","required":True,
   "old":r'(обратиться по адресу:\s*)`?blagorussia@yandex\.ru`?',
   "new":r'\1`webmaster@blagorussia.ru` ⚠️ До завершения Миграционного Этапа 1 fallback: `blagorussia@yandex.ru`',
   "desc":"САМ Г5: email для 152-ФЗ -> webmaster + fallback (SAM-INFRA-013)"},
  {"file":"СУМКа.md","type":"regex","required":True,
   "old":r'(\|\s*Корпоративная почта\s*\|\s*`?webmaster@blagorussia\.ru`?\s*\|\s*)Яндекс 360 для НКО \(бесплатно\)(\s*\|)',
   "new":r'\1Яндекс 360 для НКО (бесплатно). ⚠️ Активируется как основной после завершения Миграционного Этапа 1; до этого fallback: `blagorussia@yandex.ru`\2',
   "desc":"СУМКа 8.2: пометка активации webmaster (SAM-INFRA-013)"},
  {"file":"МИГРАЦИЯ.md","type":"regex","required":True,
   "old":r'деплоится на GitHub Pages \(аккаунт `?blago-nko`?\)',
   "new":'деплоится на **Vercel (аккаунт `can-secure-dev`)** для сохранения изоляции ПДн-контура. Деплой в публичный аккаунт `blago-nko` (GitHub Pages) **ЗАПРЕЩЕН**',
   "desc":"МИГРАЦИЯ 5.1.4: изоляция САН на Vercel (SAM-MIG-005) ч.1"},
  {"file":"МИГРАЦИЯ.md","type":"regex","required":True,
   "old":r'\s*вместе с остальными 13 контентными сайтами',
   "new":'',
   "desc":"МИГРАЦИЯ 5.1.4: убрать совместный деплой (SAM-MIG-005) ч.2"},
  {"file":"МИГРАЦИЯ.md","type":"regex","required":True,
   "old":r'(DNS для `?can\.blagorussia\.ru`? временно смотрит на )GitHub Pages',
   "new":r'\1Vercel',
   "desc":"МИГРАЦИЯ 5.1.4: DNS -> Vercel (SAM-MIG-005) ч.3"},
]

def run(*a):
    r = subprocess.run(list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def main():
    files = sorted(set(p["file"] for p in PATCHES))
    for f in files:
        if not os.path.exists(f):
            print(f"❌ Файл не найден: {f}"); sys.exit(1)
    contents = {f: open(f, encoding="utf-8").read() for f in files}

    problems = []
    for p in PATCHES:
        c = contents[p["file"]]
        n = c.count(p["old"]) if p["type"]=="lit" else len(re.findall(p["old"], c))
        if n == 0 and p["required"]:
            problems.append(f"НЕ НАЙДЕНО [{p['desc']}]: {p['old'][:70]}")
        elif p["type"]=="lit" and n > 1:
            problems.append(f"НАЙДЕНО {n} раз вместо 1 [{p['desc']}]")
    if problems:
        print("❌ Проверка не пройдена. НИЧЕГО не изменено:")
        for x in problems: print("   -", x)
        sys.exit(1)

    for p in PATCHES:
        f, c = p["file"], contents[p["file"]]
        if p["type"]=="lit":
            contents[f] = c.replace(p["old"], p["new"]); print("✅", p["desc"])
        else:
            newc, n = re.subn(p["old"], p["new"], c)
            if n: contents[f] = newc; print("✅", p["desc"])
            else: print("⏭ пропуск:", p["desc"])
    for f, c in contents.items():
        open(f, "w", encoding="utf-8").write(c)
    print("\n💾 Файлы обновлены.")

    if os.path.exists("САН.md"):
        print("\n🔍 Строки с 'CC BY' в САН.md (проверьте вручную при необходимости):")
        for i, line in enumerate(open("САН.md", encoding="utf-8"), 1):
            if "CC BY" in line:
                print(f"   САН.md:{i}: {line.strip()[:130]}")

    if os.path.exists("scripts/sync_manifests.py"):
        print("\n🔄 Запуск scripts/sync_manifests.py ...")
        r = subprocess.run([sys.executable, "scripts/sync_manifests.py"], capture_output=True, text=True)
        print(r.stdout[-1500:])
        if r.returncode != 0: print("⚠️ sync ошибка:\n", r.stderr[-1500:])

    _, out = run("git", "status", "--porcelain")
    if not out.strip():
        print("ℹ️ Нет изменений для коммита."); return
    _, name = run("git", "config", "user.name")
    if not name.strip(): run("git", "config", "user.name", "Architecture Bot")
    _, email = run("git", "config", "user.email")
    if not email.strip(): run("git", "config", "user.email", "bot@blago-nko.local")
    run("git", "checkout", "-B", BRANCH)
    run("git", "add", "-A")
    run("git", "commit", "-m", COMMIT_MSG)
    code, out = run("git", "push", "-u", "origin", BRANCH, "--force")
    print("\n" + out)
    _, remote = run("git", "config", "--get", "remote.origin.url")
    m = re.search(r'github\.com[:/]([\w.-]+/[\w.-]+?)(\.git)?$', remote.strip())
    if m:
        print(f"\n🔗 СОЗДАТЬ PR: https://github.com/{m.group(1)}/compare/main...{BRANCH}?expand=1")

if __name__ == "__main__":
    main()