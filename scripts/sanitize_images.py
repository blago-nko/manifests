#!/usr/bin/env python
"""Image Sanitization Pipeline (САМ 2.5): EXIF -> WebP -> ресайз <=1600 -> дедуп.
Зависимости: pip install Pillow (опционально imagehash)."""
import argparse, hashlib, sys
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    sys.exit("Ошибка: pip install Pillow")

SIZES = (400, 800, 1200, 1600)
MAX = 1600

def phash(path):
    try:
        import imagehash
        return str(imagehash.phash(Image.open(path)))
    except Exception:
        return hashlib.md5(Path(path).read_bytes()).hexdigest()

def sanitize(src, out_dir, seen=None):
    src, out_dir = Path(src), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGB")
    w, h = img.size
    if max(w, h) > MAX:
        k = MAX / max(w, h)
        img = img.resize((int(w * k), int(h * k)), Image.LANCZOS)
    outs = []
    for s in SIZES:
        im = img.copy()
        w, h = im.size
        if max(w, h) > s:
            k = s / max(w, h)
            im = im.resize((int(w * k), int(h * k)), Image.LANCZOS)
        p = out_dir / f"{src.stem}_{s}.webp"
        im.save(p, "WEBP", quality=82)
        outs.append(p)
    d = phash(outs[-1])
    if seen is not None:
        if d in seen:
            return None
        seen.add(d)
    return outs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    seen, ok, dup = set(), 0, 0
    for f in sorted(Path(a.src).rglob("*")):
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            r = sanitize(f, a.out, seen)
            ok, dup = ok + (1 if r else 0), dup + (0 if r else 1)
    print(f"Готово: обработано {ok}, дубликатов {dup}")

if __name__ == "__main__":
    main()
