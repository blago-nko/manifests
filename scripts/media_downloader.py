#!/usr/bin/env python3
"""Скачивание медиа в локальный /static/images/ (MIG-002)."""
import argparse
import hashlib
import re
from pathlib import Path
from urllib.parse import unquote

try:
    import requests
except ImportError:
    print("ERROR: установите requests: pip install requests")
    raise SystemExit(1)


def extract_image_urls(markdown_content):
    """Извлечь URL изображений из markdown и figure/img."""
    urls = re.findall(r'!\[[^\]]*\]\(([^)\s]+)', markdown_content)
    urls += re.findall(r'\{\{< imgfigure src="([^"]+)"', markdown_content)
    seen = set()
    result = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def safe_filename(url):
    """Имя файла: декодировать, санитизировать, hash для длинных имён."""
    raw = url.split("/")[-1].split("?")[0]
    name = unquote(unquote(raw))
    name = re.sub(r'[\\/:*?"<>|]', "-", name)
    name = name.replace(" ", "-")
    ext = ""
    dot = name.rfind(".")
    if dot != -1 and len(name) - dot <= 5:
        ext = name[dot:]
        name = name[:dot]
    if len(name) > 80:
        name = hashlib.md5(url.encode("utf-8")).hexdigest()[:16]
    return name + ext


def download_image(url, output_dir):
    """Скачать изображение и вернуть локальный путь."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    filename = safe_filename(url)
    output_path = output_dir / filename
    output_path.write_bytes(response.content)
    return f"images/{filename}"


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
        for url in extract_image_urls(content):
            if url.startswith("http://") or url.startswith("https://"):
                try:
                    local_path = download_image(url, output_dir)
                    content = content.replace(url, local_path)
                    print(f"Скачано: {url[:80]}... -> {local_path}")
                except Exception as e:
                    print(f"Ошибка скачивания {url[:80]}...: {e}")
        post_file.write_text(content, encoding="utf-8")

    print(f"Скачивание завершено: {output_dir}")


if __name__ == "__main__":
    main()
