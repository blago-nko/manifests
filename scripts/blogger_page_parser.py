#!/usr/bin/env python
"""Полноценный парсер Blogger по известным URL (MIG-005, MIG-015).
Вход: каталог aliases/ или seo-redirects/ ИЛИ migration_seo_map.json.
Выход: Hugo-Markdown (content/posts/) + media_passport.json.gz.

Извлекает: title, date, description (сниппет), body (post-body), labels,
изображения (нормализация /s1600/), видео (в паспорт для Видео-Матрицы).
Комментарии НЕ мигрируют (MIG-015). Idempotent. Throttling 1 req/s.

Использование:
  python blogger_page_parser.py --aliases-dir ~/Projects/novosti/content/aliases \
      --domain novosti.blagorussia.ru --out-dir ~/Projects/novosti
  python blogger_page_parser.py --seo-map ~/Projects/blagorussia.ru/data/blogger/migration_seo_map.json \
      --domain blagorussia.blogspot.com --out-dir ~/Projects/blagorussia.ru
"""
import argparse, gzip, json, re, sys, time, urllib.request
from pathlib import Path

def fetch(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (blago-migration)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:
            if i == retries - 1:
                print(f"  ! ошибка {url}: {e}")
                return None
            time.sleep(2 ** i)

def extract_title(h):
    m = re.search(r"<title>([^<]+)</title>", h, re.I)
    return m.group(1).strip() if m else ""

def extract_date(h):
    for pat in (r'"datePublished"\s*:\s*"([^"]+)"', r'"published"\s*:\s*"([^"]+)"',
                r'<time[^>]+datetime="([^"]+)"', r"<published>([^<]+)</published>"):
        m = re.search(pat, h)
        if m:
            return m.group(1)[:10]
    return ""

def extract_description(h, body_md):
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', h, re.I)
    if m and m.group(1).strip():
        return m.group(1).strip()
    m = re.search(r'"description"\s*:\s*"([^"]{10,})"', h)
    if m:
        return m.group(1)
    return re.sub(r"[\n\s]+", " ", body_md).strip()[:160]

def extract_body(h):
    m = re.search(r'<div[^>]*class=["\'][^"\']*\bpost-body\b[^"\']*["\'][^>]*>(.*?)(?:<div class="post-footer|<div class="comments|<div id="comments|$)', h, re.I | re.S)
    return m.group(1) if m else ""

def extract_labels(h):
    tags = re.findall(r'rel="tag"[^>]*>\s*([^<]+?)\s*</a>', h)
    if tags:
        return [t.strip() for t in tags[:10]]
    m = re.search(r'class="post-labels"[^>]*>(.*?)</span>', h, re.I | re.S)
    if m:
        return [x.strip() for x in re.findall(r">([^<]+)<", m.group(1)) if x.strip()][:10]
    m = re.search(r'data-labels="([^"]+)"', h)
    if m:
        return [x.strip() for x in m.group(1).split(",") if x.strip()][:10]
    return []

def extract_images(html):
    return re.findall(r'<img[^>]+src=["\'](https://(?:blogger\.googleusercontent\.com|[^"\']*blogspot\.com)[^"\']+)["\']', html)

def extract_videos(html):
    vids = [v for v in re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', html, re.I)
            if re.search(r"video\.g|youtube\.com/embed|vk\.com/video|rutube\.ru/embed", v, re.I)]
    vids += re.findall(r"<source[^>]+src=[\"\']([^\"\']+)[\"\']", html, re.I)
    return vids

def fix_size(u):
    return re.sub(r"/s\d+(-rw)?/", "/s1600/", u)

def html_to_markdown(html):
    try:
        import markdownify
        return markdownify.markdownify(html, heading_style="ATX")
    except ImportError:
        pass
    h = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{m.group(2)}]({m.group(1)})", html, flags=re.S)
    h = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", h, flags=re.S)
    h = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", h, flags=re.S)
    h = re.sub(r"<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", h)
    h = re.sub(r"</h[1-6]>", "\n\n", h)
    h = re.sub(r"<li[^>]*>", "\n- ", h)
    h = re.sub(r"<(p|div|br)[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    return re.sub(r"\n{3,}", "\n\n", h).strip()

def parse_url(old_url, domain, out_dir, passport):
    slug = Path(old_url).stem or re.sub(r"[^a-z0-9-]", "-", old_url.lower())[:60]
    md_path = out_dir / f"{slug}.md"
    if md_path.exists():
        return 0
    html = fetch(f"https://{domain}{old_url}")
    if not html:
        return -1
    title = extract_title(html)
    date = extract_date(html)
    body_html = extract_body(html)
    labels = extract_labels(html)
    videos = extract_videos(html)
    for img in extract_images(body_html):
        body_html = body_html.replace(img, fix_size(img))
        passport.append({"post": slug, "type": "image", "src": img, "resized": fix_size(img)})
    for v in videos:
        passport.append({"post": slug, "type": "video", "src": v, "status": "requires_video_matrix"})
    body_md = html_to_markdown(body_html)
    desc = extract_description(html, body_md)
    fm = ["---", f'title: "{title.replace(chr(34), chr(39))}"']
    if date:
        fm.append(f"date: {date}")
    if desc:
        fm.append(f'description: "{desc.replace(chr(34), chr(39))}"')
    fm += ["aliases:", f'  - "{old_url}"']
    if labels:
        fm += ["tags:"] + [f"  - {t}" for t in labels]
    fm += ["---", "", body_md, ""]
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(fm), encoding="utf-8")
    return 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aliases-dir")
    ap.add_argument("--seo-map")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    out_dir = Path(a.out_dir).expanduser() / "content" / "posts"
    out_dir.mkdir(parents=True, exist_ok=True)
    urls = []
    if a.aliases_dir:
        for f in Path(a.aliases_dir).expanduser().rglob("*.md"):
            m = re.search(r'aliases:\s*\n\s*-\s*"([^"]+)"', f.read_text(encoding="utf-8"))
            if m:
                urls.append(m.group(1))
    elif a.seo_map:
        urls = list(json.load(open(a.seo_map, encoding="utf-8")).get("redirects", {}).keys())
    else:
        sys.exit("Ошибка: укажите --aliases-dir или --seo-map")
    print(f"URL для парсинга: {len(urls)}")
    passport, ok, skip, err = [], 0, 0, 0
    for i, u in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {u}")
        r = parse_url(u, a.domain, out_dir, passport)
        ok, skip, err = ok + (r == 1), skip + (r == 0), err + (r == -1)
        time.sleep(1)
    if passport:
        with gzip.open(Path(a.out_dir).expanduser() / "media_passport.json.gz", "wt", encoding="utf-8") as f:
            json.dump(passport, f, ensure_ascii=False)
    print(f"\nГотово: новых {ok}, пропущено {skip}, ошибок {err}; в паспорте {len(passport)}")

if __name__ == "__main__":
    main()
