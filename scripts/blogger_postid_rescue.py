#!/usr/bin/env python
"""Rescue через postID с защитой от ошибок фида."""
import json, re, sys, time, hashlib
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0, str(Path.home()/'Projects/manifests/scripts'))
from blogger_page_parser import fetch, extract_images, fix_size, html_to_markdown

def main():
    blog_id, missing_file, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])/'content'/'posts'
    out_dir.mkdir(parents=True, exist_ok=True)
    missing = ['/' + l.strip().lstrip('/') for l in Path(missing_file).read_text().splitlines() if l.strip()]
    months = sorted({tuple(m.split('/')[1:3]) for m in missing if re.match(r'/\d{4}/\d{2}/', m)})
    print(f"Пропущено: {len(missing)}; месяцев: {len(months)}")

    url2pid = {}
    for y, mo in months:
        html = fetch(f"https://www.blagorussia.ru/{y}_{mo}_01_archive.html") or ""
        found = re.findall(r"postID=(\d+)[^>]{0,300}?data-url='([^']+)'", html)
        for pid, url in found:
            url2pid[urlparse(url).path] = pid
        print(f"  {y}/{mo}: postID: {len(found)}")
        time.sleep(0.5)

    ok = 0
    for m in missing:
        pid = url2pid.get(m)
        if not pid:
            print(f"  ! нет postID: {m}"); continue
        slug = re.sub(r"[^a-z0-9-]", "-", Path(m).stem.lower())[:60]
        fname = slug if len(slug) <= 100 else slug[:80] + "-" + hashlib.md5(slug.encode()).hexdigest()[:8]
        if (out_dir / f"{fname}.md").exists():
            print(f"  = уже есть: {m}"); continue
        
        raw = fetch(f"https://www.blogger.com/feeds/{blog_id}/posts/default/{pid}?alt=json")
        if not raw:
            print(f"  ! fetch пуст: {m}"); continue
        
        try:
            e = json.loads(raw)
        except Exception as ex:
            print(f"  ! JSON error: {m} ({ex})"); continue
        
        if "entry" not in e:
            print(f"  ! нет entry: {m} (keys: {list(e.keys())[:5]})"); continue
        
        entry = e["entry"]
        if "title" not in entry or "content" not in entry:
            print(f"  ! нет title/content: {m} (entry keys: {list(entry.keys())[:5]})"); continue
        
        body = entry.get("content", {}).get("$t", "")
        for img in extract_images(body):
            body = body.replace(img, fix_size(img))
        md = html_to_markdown(body)
        fm = ["---", f'title: "{entry["title"]["$t"].replace(chr(34), chr(39))}"',
              f'date: {entry["published"]["$t"][:10]}',
              "aliases:", f'  - "{m}"', f'url: "/{slug}/"',
              "---", "", md, ""]
        (out_dir / f"{fname}.md").write_text("\n".join(fm), encoding="utf-8")
        ok += 1
        print(f"  + {m}")
        time.sleep(0.5)
    print(f"\nСпасено: {ok} из {len(missing)}")

if __name__ == "__main__":
    main()
