#!/usr/bin/env python3
"""Скачивание медиа из Blogger в локальный /static/images/ (MIG-002)."""
import argparse
import re
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: установите requests: pip install requests")
    raise SystemExit(1)


def extract_image_urls(markdown_content):
    """Извлечь URL изображений из markdown."""
    pattern = r"!\[.*?\]\((.*?)\)"
    return re.findall(pattern, markdown_content)


def download_image(url, output_dir):
    """Скачать изображение и вернуть локальный путь."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    filename = url.split("/")[-1].split("?")[0]
    output_path = output_dir / filename
    output_path.write_bytes(response.content)
    return f"/images/{filename}"


def main():
    parser = argparse.ArgumentParser(description="Скачивание медиа из постов")
    parser.add_argument("--content-dir", default="content/posts")
    parser.add_argument("--output-dir", default="static/images")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for post_file in content_dir.glob("*.md"):
        content = post_file.read_text(encoding="utf-8")
        image_urls = extract_image_urls(content)
        for url in image_urls:
            if "blogger.com" in url or "blogspot.com" in url:
                try:
                    local_path = download_image(url, output_dir)
                    content = content.replace(url, local_path)
                    print(f"Скачано: {url} -> {local_path}")
                except Exception as e:
                    print(f"Ошибка скачивания {url}: {e}")
        post_file.write_text(content, encoding="utf-8")

    print(f"Скачивание завершено: {output_dir}")


if __name__ == "__main__":
    main()
