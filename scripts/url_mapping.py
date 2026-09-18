#!/usr/bin/env python3
"""Маппинг старых URL -> новых для 301-редиректов (MIG-002)."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Генерация маппинга URL")
    parser.add_argument("--content-dir", default="content/posts")
    parser.add_argument("--output", default="data/url_mapping.json")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    mapping = {}

    for post_file in content_dir.glob("*.md"):
        content = post_file.read_text(encoding="utf-8")
        if "blogger_url:" in content:
            lines = content.split("\n")
            for line in lines:
                if line.startswith("blogger_url:"):
                    old_url = line.split(":", 1)[1].strip().strip('"')
                    slug = post_file.stem
                    date_line = next((l for l in lines if l.startswith("date:")), None)
                    if date_line:
                        date_str = date_line.split(":", 1)[1].strip().strip('"')
                        year, month = date_str.split("-")[:2]
                        new_url = f"/{year}/{month}/{slug}.html"
                        mapping[old_url] = new_url
                    break

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Маппинг сохранён: {output_path} ({len(mapping)} URL)")


if __name__ == "__main__":
    main()
