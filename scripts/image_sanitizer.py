#!/usr/bin/env python3
"""
Image Sanitizer for blago-nko ecosystem.
Requirements: МИГРАЦИЯ.md p.5.1.1.7, САМ p.2.4, p.2.5.

Pipeline:
1. Download original from source URL (handled by caller/media_downloader.py).
2. Strip EXIF metadata (privacy/security).
3. Resize to max dimension <= 1600px (preserve aspect ratio).
4. Apply Watermark (brand protection, optional flag).
5. Calculate pHash (deduplication).
6. Convert to WebP/JPEG (optimization).
7. Output processed file path and metadata.
"""

import os
import sys
import argparse
from PIL import Image
import io

try:
    import imagehash
except ImportError:
    print("❌ Error: Library 'ImageHash' is missing. Run: pip install ImageHash")
    sys.exit(1)

def strip_exif(img):
    """Remove all EXIF data by creating a clean copy."""
    try:
        # Создаем новое изображение того же размера и режима
        clean_img = Image.new(img.mode, img.size)
        # Вставляем пиксели оригинала в чистый холст
        clean_img.paste(img, (0, 0))
        return clean_img
    except Exception as e:
        print(f"Warning: Failed to strip EXIF: {e}")
        return img

def resize_image(img, max_dim=1600):
    """Resize image so that the largest side is <= max_dim pixels."""
    width, height = img.size

    if width <= max_dim and height <= max_dim:
        return img

    scale_factor = min(max_dim / float(width), max_dim / float(height))
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Use LANCZOS for high-quality downsampling
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    return resized_img

def apply_watermark(img, watermark_path='assets/watermark.png'):
    """Apply NGO watermark to the bottom-right corner."""
    if not os.path.exists(watermark_path):
        print(f"⚠️ Watermark file not found: {watermark_path}. Skipping.")
        return img
        
    try:
        with Image.open(watermark_path) as wm:
            # Ensure RGBA mode for transparency support
            if wm.mode != 'RGBA':
                wm = wm.convert('RGBA')
            
            # Position: Bottom Right with padding
            padding = 20
            x_pos = img.width - wm.width - padding
            y_pos = img.height - wm.height - padding
            
            # Paste watermark onto image using itself as mask
            img.paste(wm, (x_pos, y_pos), wm)
            
        return img
    except Exception as e:
        print(f"❌ Error applying watermark: {e}")
        return img

def calculate_phash(img):
    """Calculate perceptual hash for deduplication."""
    try:
        # imagehash expects a PIL Image object
        phash = str(imagehash.phash(img))
        return phash
    except Exception as e:
        print(f"Warning: Failed to calculate pHash: {e}")
        return None

def process_image(input_path, output_dir=None, format='WEBP', add_watermark=False):
    """Main processing function."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        with Image.open(input_path) as img:
            # Capture original dimensions before modification
            orig_w, orig_h = img.size

            # Ensure RGB mode for JPEG/WebP compatibility (flattening alpha if present)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                 # Option A: Flatten to white background for JPG/WebP
                 bg = Image.new("RGB", img.size, (255, 255, 255))
                 bg.paste(img, mask=img.split()[3]) # 3 is the alpha channel
                 img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Step 1: Strip EXIF
            img = strip_exif(img)

            # Step 2: Resize
            img = resize_image(img, max_dim=1600)

            # Step 3: Apply Watermark (New!)
            if add_watermark:
                img = apply_watermark(img)

            # Step 4: Calculate pHash (New!)
            phash_value = calculate_phash(img)

            # Determine output filename
            base_name = os.path.basename(input_path)
            name_parts = os.path.splitext(base_name)
            ext = '.webp' if format.upper() == 'WEBP' else '.jpg'
            out_filename = f"{name_parts[0]}_sanitized{ext}"

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                out_path = os.path.join(output_dir, out_filename)
            else:
                out_path = input_path.replace(name_parts[1], '_sanitized' + ext)

            # Save optimized image
            save_kwargs = {'quality': 85, 'optimize': True}
            if format.upper() == 'WEBP':
                save_kwargs['method'] = 6
                
            img.save(out_path, format=format.upper(), **save_kwargs)

            # Return structured result for caller (e.g., uploader script)
            return {
                "status": "success",
                "path": out_path,
                "phash": phash_value,
                "original_size": [orig_w, orig_h],
                "final_size": list(img.size)
            }

    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sanitize images for blago-nko")
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("--output-dir", "-o", help="Directory for sanitized output")
    parser.add_argument("--format", "-f", default="WEBP", choices=["WEBP", "JPEG"], help="Output format")
    parser.add_argument("--watermark", "-w", action="store_true", help="Apply NGO watermark")

    args = parser.parse_args()

    result = process_image(args.input, args.output_dir, args.format, add_watermark=args.watermark)
    
    if result["status"] == "success":
        print(f"✅ Success: {result['path']} | Hash: {result['phash']}")
        sys.exit(0)
    else:
        print(f"❌ Failure: {result.get('message')}")
        sys.exit(1)
