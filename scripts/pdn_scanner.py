#!/usr/bin/env python
"""Сканер персональных данных (ПДн) в Markdown-файлах.
Находит: телефоны, email, паспорта, ФИО (русские), адреса, даты рождения."""
import re, sys
from pathlib import Path

PATTERNS = {
    'phone_ru': re.compile(r'(?:\+7|8)[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}'),
    'phone_short': re.compile(r'(?<!\d)[2-9]\d{2}[\-\s]\d{2}[\-\s]\d{2}(?!\d)'),
    'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    'passport_ru': re.compile(r'\b[0-9]{4}\s?[0-9]{6}\b'),
    'snils': re.compile(r'\b[0-9]{3}\s?[0-9]{3}\s?[0-9]{3}\s?[0-9]{2}\b'),
    'inn_phys': re.compile(r'\b[0-9]{12}\b'),
    'date_birth': re.compile(r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}\b'),
    'address_keyword': re.compile(r'(?:ул\.|улица|пр\.|проспект|пер\.|переулок|д\.|дом|кв\.|квартира|г\.\s*\w+)[^,.]{0,80}(?:д\.\s*\d+|дом\s+\d+)', re.I),
    'fio_pattern': re.compile(r'[А-ЯЁ][а-яё]{1,20}\s+[А-ЯЁ][а-яё]{1,20}\s+[А-ЯЁ][а-яё]{1,20}'),
}

def scan_file(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    findings = {}
    for name, pat in PATTERNS.items():
        matches = pat.findall(text)
        if matches:
            findings[name] = matches[:5]  # максимум 5 примеров на тип
    return findings

def main():
    repo = Path(sys.argv[1])
    posts = repo / 'content' / 'posts'
    if not posts.exists():
        print(f"{repo}: нет content/posts"); return
    total = {}; files_with_pdn = 0
    for f in posts.glob('*.md'):
        found = scan_file(f)
        if found:
            files_with_pdn += 1
            print(f"\n{f.name}:")
            for k, v in found.items():
                total.setdefault(k, []).extend(v)
                print(f"  {k}: {v}")
    print(f"\n=== ИТОГО по {repo.name} ===")
    print(f"Файлов с ПДн: {files_with_pdn}")
    for k, v in total.items():
        print(f"  {k}: {len(v)} (примеры: {v[:3]})")

if __name__ == "__main__":
    main()
