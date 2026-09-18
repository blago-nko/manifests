#!/usr/bin/env python3
"""Экспорт постов из Blogger API -> YAML front matter + markdown (MIG-002)."""
import argparse
import json
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


def convert_html_to_markdown(html_content):
    """Простая конвертация HTML -> markdown."""
    text = html_content
    text = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n\n", text, flags=re.DOTALL)
    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL)
    text = re.sub(r"<(?:b|strong)[^>]*>(.*?)</(?:b|strong)>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<(?:i|em)[^>]*>(.*?)</(?:i|em)>", r"*\1*", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def create_front_matter(post):
    """Создать YAML front matter из поста Blogger."""
    published = datetime.fromisoformat(post["published"].replace("Z", "+00:00"))
    slug = post["url"].split("/")[-1].replace(".html", "")
    labels = post.get("labels", [])
    categories = labels[:1] if labels else ["общее"]
    tags = labels[1:] if len(labels) > 1 else []

    front_matter = {
        "title": post["title"],
        "date": published.strftime("%Y-%m-%d"),
        "draft": False,
        "description": post.get("title", "")[:160],
        "tags": tags,
        "categories": categories,
        "author": "blago-nko",
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
