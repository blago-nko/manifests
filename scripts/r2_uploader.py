#!/usr/bin/env python3
"""
Uploader for Cloudflare R2 using boto3.
Supports single file upload and batch directory processing.

Usage:
  # Single file
  python scripts/r2_uploader.py --file path/to/image.jpg --folder new-content
  
  # Batch (entire folder)
  python scripts/r2_uploader.py --dir assets/incoming --folder legacy-migration

Requires environment variables:
  R2_ACCESS_KEY_ID
  R2_SECRET_ACCESS_KEY
  R2_ENDPOINT_URL
  R2_BUCKET_NAME
  R2_PUBLIC_DOMAIN (optional, defaults to https://cdn.obrazslov.ru)
"""

import os
import sys
import argparse
import mimetypes
from pathlib import Path

try:
    import boto3
    from botocore.client import Config
except ImportError:
    print("❌ Missing library 'boto3'. Run: pip install boto3")
    sys.exit(1)

class R2Uploader:
    def __init__(self):
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.endpoint_url = os.getenv('R2_ENDPOINT_URL')
        self.bucket_name = os.getenv('R2_BUCKET_NAME')
        self.public_domain = os.getenv('R2_PUBLIC_DOMAIN', 'https://cdn.obrazslov.ru')
        
        if not all([self.access_key, self.secret_key, self.endpoint_url, self.bucket_name]):
            raise EnvironmentError(
                "Missing required R2 environment variables.\n"
                "Set: R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL, R2_BUCKET_NAME"
            )

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )

    def _get_mime_type(self, filepath):
        mime_type, _ = mimetypes.guess_type(str(filepath))
        return mime_type or 'application/octet-stream'

    def upload_file(self, local_path, remote_folder='new-content'):
        """Uploads a single file to R2."""
        file_path = Path(local_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")
            
        filename = file_path.name
        object_key = f"{remote_folder}/{filename}"
        
        extra_args = {'ContentType': self._get_mime_type(file_path)}
        
        print(f"📤 Uploading {local_path} to r2://{object_key}...", end="", flush=True)
        try:
            self.s3_client.upload_file(str(file_path), self.bucket_name, object_key, ExtraArgs=extra_args)
            public_url = f"{self.public_domain}/{object_key}"
            print(f" ✅ Done!\n   🔗 URL: {public_url}")
            return public_url
        except Exception as e:
            print(f" ❌ Failed: {e}")
            return None

    def upload_directory(self, dir_path, remote_folder='new-content'):
        """Recursively uploads all files in a directory."""
        results = []
        dir_path = Path(dir_path)
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")
            
        files = list(dir_path.rglob("*"))
        total = len(files)
        print(f"📂 Found {total} files in {dir_path}. Starting batch upload...")
        
        for i, file_path in enumerate(files, 1):
            if file_path.is_file():
                rel_path = file_path.relative_to(dir_path)
                # Preserve subdirectory structure in R2
                target_folder = f"{remote_folder}/{rel_path.parent}" if str(rel_path.parent) != "." else remote_folder
                
                url = self.upload_file(file_path, target_folder)
                if url:
                    results.append({'local': str(file_path), 'url': url})
                
                # Progress indicator
                progress = int((i / total) * 100)
                print(f"   [{progress}%] Processed {i}/{total}", end='\r')
        
        print("\n\n🏁 Batch upload complete.")
        return results

def main():
    parser = argparse.ArgumentParser(description="Upload files to Cloudflare R2")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to a single file to upload")
    group.add_argument("--dir", help="Path to a directory to recursively upload")
    
    parser.add_argument("--folder", default="new-content", 
                        help="Remote folder prefix in the bucket (default: new-content)")
    
    args = parser.parse_args()

    try:
        uploader = R2Uploader()
        
        if args.file:
            url = uploader.upload_file(args.file, args.folder)
            if url:
                print(f"\nTo use in Markdown:\n![alt text]({url})")
        elif args.dir:
            results = uploader.upload_directory(args.dir, args.folder)
            # Optional: Save mapping to JSON for later reference
            if results:
                with open('r2_upload_map.json', 'w') as f:
                    import json
                    json.dump(results, f, indent=2)
                print("💾 Mapping saved to 'r2_upload_map.json'")
                
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
