#!/usr/bin/env python
"""IImageStorage — адаптер хранилища изображений (САМ 2.1).
Абстрактный интерфейс: позволяет менять хранилище (Blogger/R2)
без изменения бизнес-логики миграции.
Реализация для галереи: web-gallery-npo/scripts/gallery_uploader.py"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
import re

class IImageStorage(ABC):
    @abstractmethod
    def normalize_url(self, url: str) -> str:
        """Нормализовать URL изображения (размер, формат)."""

    @abstractmethod
    def upload_image(self, local_path: Path, metadata: Optional[Dict] = None) -> str:
        """Загрузить локальное изображение, вернуть URL."""

    @abstractmethod
    def create_gallery_post(self, title: str, image_urls: List[str],
                            labels: Optional[List[str]] = None) -> str:
        """Создать пост-галерею, вернуть URL поста."""

    def sanitize_size_in_url(self, url: str, target_size: int = 1600) -> str:
        """САМ 1.9: размер <=1600px для безлимита Blogger."""
        return re.sub(r"/s\d+(-rw)?/", f"/s{target_size}/", url)
