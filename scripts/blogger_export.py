#!/usr/bin/env python3
"""Экспорт постов из Blogger API -> YAML front matter + markdown (MIG-002)."""
import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: установите requests: pip install requests")
    raise SystemExit(1)


def fetch_blogger_posts(blog_id, api_key):
    """Получить все посты из Blogger API."""
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"
    params = {"key": api_key, "maxResults": 500}
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json().get("items", [])


def _img_attrs(tag):
    """Извлечь src и alt из тега img."""
    src = re.search(r'src="([^"]+)"', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    return (src.group(1) if src else ""), (alt.group(1) if alt else "")


def _figure(src, alt, caption=""):
    """Собрать шорткод imgfigure: relURL в шаблоне, alt/title/caption."""
    alt = (alt or "").strip().replace('"', "'")
    cap = (caption or "").strip() or alt
    sc = (
        '{{< img src="' + src + '" alt="' + (alt or cap)
        + '" title="' + cap + '" caption="' + cap + '" >}}'
    )
    return sc, cap


def _collapse(inner):
    """Схлопнуть одиночные переносы в пробел, сохранив разрывы абзацев."""
    inner = re.sub(r"\n{2,}", "@@PB@@", inner)
    inner = re.sub(r"\s*\n\s*", " ", inner)
    return inner.replace("@@PB@@", "\n\n")


def convert_html_to_markdown(html_content):
    """Конвертация HTML Blogger -> markdown; figure/iframe/center через плейсхолдеры."""
    placeholders = []
    captions = {}

    def _stash(pair):
        html_block, cap = pair
        idx = len(placeholders)
        placeholders.append(html_block)
        captions[idx] = cap
        return f"\n\n@@BLOCK{idx}@@\n\n"

    def _run(text, allow_center=True):
        text = text.replace("\u00a0", " ").replace("&nbsp;", " ")

        def _keep_iframe(m):
            return _stash((m.group(0), ""))

        def _img_in_link(m):
            return _stash(_figure(*_img_attrs(m.group(1)), caption=(m.group(2) or "")))

        def _img_solo(m):
            return _stash(_figure(*_img_attrs(m.group(1)), caption=(m.group(2) or "")))

        def _center(m):
            inner = _run(m.group(1), allow_center=False)
            return _stash((f'<div class="text-center">\n\n{inner}\n\n</div>', ""))

        cap_tail = r'(?:\s*<span[^>]*>(.*?)</span>)?'

        text = re.sub(r"<iframe[^>]*>.*?</iframe>", _keep_iframe, text, flags=re.DOTALL)
        if allow_center:
            text = re.sub(r'<div[^>]*?text-align:\s*center[^>]*?>(.*?)</div>', _center, text, flags=re.DOTALL)
        text = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1\n\n", text, flags=re.DOTALL)
        text = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n\n", text, flags=re.DOTALL)
        text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n\n", text, flags=re.DOTALL)
        text = re.sub(r"<h4[^>]*>(.*?)</h4>", r"#### \1\n\n", text, flags=re.DOTALL)
        text = re.sub(
            r'<a[^>]*href="[^"]*"[^>]*>\s*(<img[^>]*?>)\s*</a>' + cap_tail,
            _img_in_link,
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"(<img[^>]*?>)" + cap_tail, _img_solo, text, flags=re.DOTALL)
        text = re.sub(
            r"<li[^>]*>(.*?)</li>",
            lambda m: "- " + re.sub(r"\s*\n\s*", " ", m.group(1)).strip() + "\n",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"</?(?:ul|ol)[^>]*>", "\n", text)
        text = re.sub(r"<br\s*/?>", "\n\n", text)
        text = re.sub(r'<p[^>]*?text-align:\s*center[^>]*?>(.*?)</p>', _center, text, flags=re.DOTALL)
        text = re.sub(
            r"<p[^>]*>(.*?)</p>",
            lambda m: _collapse(m.group(1)) + "\n\n",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            lambda m: "[" + re.sub(r"\s+", " ", m.group(2)).strip() + "](" + m.group(1) + ")",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)([».)])", r"[\1\3](\2)", text)
        text = re.sub(r"<(?:b|strong)[^>]*>(.*?)</(?:b|strong)>", r"**\1**", text, flags=re.DOTALL)
        text = re.sub(r"<(?:i|em)[^>]*>(.*?)</(?:i|em)>", r"*\1*", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", "", text)
        return text

    text = _run(html_content)
    for i in range(len(placeholders) - 1, -1, -1):
        text = text.replace(f"@@BLOCK{i}@@", placeholders[i])
    for i, cap in captions.items():
        if cap:
            text = re.sub(r" >\}\}\s*" + re.escape(cap), " >}}\n", text, count=1)
    text = re.sub(r"([^\n])\n([».,;:!?)])", r"\1\2", text)
    text = re.sub(r"([«(])\s*\n\s*([^\n])", r"\1\2", text)
    text = re.sub(r"([^\n])\n(?!\n)(?=[^\s\-#<@{])", r"\1 ", text)
    text = re.sub(r"([«(])\n\n", r"\1", text)
    text = re.sub(r"</a>\n", "</a>", text)
    text = re.sub(r"</a>\s*\n\n+", "</a>", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def create_front_matter(post):
    """Создать YAML front matter из поста Blogger."""
    published = datetime.fromisoformat(post["published"].replace("Z", "+00:00"))
    slug = post["url"].split("/")[-1].replace(".html", "")
    labels = post.get("labels", [])
    author = post.get("author", {}).get("displayName", "blago-nko")

    front_matter = {
        "title": post["title"],
        "date": published.strftime("%Y-%m-%d"),
        "draft": False,
        "description": post.get("title", "")[:160],
        "tags": list(labels),
        "author": author,
        "blogger_url": post["url"],
    }
    return front_matter, slug


def main():
    parser = argparse.ArgumentParser(description="Экспорт постов из Blogger")
    parser.add_argument("--blog-id", required=True, help="Blogger Blog ID")
    parser.add_argument("--api-key", required=True, help="Google API Key")
    parser.add_argument("--output-dir", default="content/posts", help="Директория для экспорта")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    posts = fetch_blogger_posts(args.blog_id, args.api_key)
    print(f"Найдено постов: {len(posts)}")

    for post in posts:
        front_matter, slug = create_front_matter(post)
        markdown = convert_html_to_markdown(post["content"])

        yaml_lines = ["---"]
        for key, value in front_matter.items():
            if isinstance(value, list):
                yaml_lines.append(f"{key}:")
                for item in value:
                    yaml_lines.append(f'  - "{item}"')
            else:
                yaml_lines.append(f'{key}: "{value}"')
        yaml_lines.append("---")
        yaml_lines.append("")
        yaml_lines.append(markdown)

        output_file = output_dir / f"{slug}.md"
        output_file.write_text("\n".join(yaml_lines), encoding="utf-8")
        print(f"Экспортирован: {output_file}")

    print(f"Экспорт завершён: {len(posts)} постов в {output_dir}")


if __name__ == "__main__":
    main()
