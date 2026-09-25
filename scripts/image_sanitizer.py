#!/usr/bin/env python3
"""
Image Sanitizer for blago-nko ecosystem.
Requirements: МИГРАЦИЯ.md p.5.1.1.7, САМ p.2.4, p.2.5.

Pipeline:
1. Download original from source URL.
2. Strip EXIF metadata (privacy/security).
3. Resize to max dimension <= 1600px (preserve aspect ratio).
4. Convert to WebP/JPEG (optimization).
5. Output processed file path or upload logic stub.
"""

import os
import sys
import argparse
from PIL import Image, ExifTags
import io

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

def process_image(input_path, output_dir=None, format='WEBP'):
    """Main processing function."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    try:
        with Image.open(input_path) as img:
            # Ensure RGB mode for JPEG/WebP compatibility
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
            
            # Step 1: Strip EXIF
            img = strip_exif(img)
            
            # Step 2: Resize
            img = resize_image(img, max_dim=1600)
            
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
            
            print(f"✅ Processed: {input_path} -> {out_path}")
            return out_path
            
    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sanitize images for blago-nko")
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("--output-dir", "-o", help="Directory for sanitized output")
    parser.add_argument("--format", "-f", default="WEBP", choices=["WEBP", "JPEG"], help="Output format")
    
    args = parser.parse_args()
    
    result = process_image(args.input, args.output_dir, args.format)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
