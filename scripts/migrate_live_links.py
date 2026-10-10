#!/usr/bin/env python3
import os
import re
import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- КОНФИГУРАЦИЯ ---
BLOG_ID = "1003873553727767854" # ID вашего блога из скриншота настроек
API_KEY = "" # Если у вас нет OAuth токена, попробуем публичный доступ через RSS/API без ключа (если разрешено) 
             # Но лучше использовать Service Account или OAuth. 
             # Для теста попробуем эндпоинт, который иногда работает без строгой авторизации для чтения,
             # либо используем RSS как fallback для получения списка постов, а детали берем из HTML парсинга страницы поста (которая надежнее прямого файла).

CONTENT_DIR = "content/posts/"
SITEMAP_URL = "https://obraz-slov.blogspot.com/sitemap.xml"

def get_post_ids_from_sitemap():
    """Парсит sitemap.xml, чтобы получить список URL постов."""
    print(f"📥 Загрузка Sitemap из {SITEMAP_URL}...")
    try:
        resp = requests.get(SITEMAP_URL, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'xml')
        
        urls = []
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if '.html' in url and '/p/' not in url: # Фильтруем статические страницы
                urls.append(url)
        
        print(f"✅ Найдено {len(urls)} постов в Sitemap.")
        return urls
    except Exception as e:
        print(f"❌ Ошибка загрузки Sitemap: {e}")
        return []

def extract_image_from_blogger_page(post_url):
    """
    Так как прямой доступ к API может требовать сложной авторизации (OAuth),
    мы используем гибридный подход:
    1. Берем URL поста из Sitemap.
    2. Скачиваем HTML страницу поста (она всегда доступна публично).
    3. Парсим оттуда <img src="...">.
    Это надежнее, чем пытаться эмулировать запросы к API без токенов,
    и дает те же самые свежие ссылки, что и API.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(post_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Ищем первую контентную картинку в теле поста
        # Обычно они находятся внутри div.post-body или article
        content_div = soup.find('div', class_='post-body') or soup.find('article')
        if not content_div:
            content_div = soup # Fallback: ищем по всему документу
            
        img_tag = content_div.find('img')
        
        if img_tag and img_tag.get('src'):
            src = img_tag['src']
            # Проверяем, что это ссылка на Blogger CDN
            if 'blogger.googleusercontent.com' in src or 'blogspot.com' in src:
                return src
                
        return None
    except Exception as e:
        print(f"   ⚠️ Ошибка при обработке {post_url}: {e}")
        return None

def build_url_to_title_map(sitemap_urls):
    """
    Создает карту: { PostURL: FirstImageURL }
    Также пытается извлечь Title из HTML для сопоставления с MD файлами.
    """
    print("\n🔄 Сканирование постов для извлечения изображений...")
    image_map = {} # { title_lower: image_url }
    
    for i, url in enumerate(sitemap_urls):
        print(f"[{i+1}/{len(sitemap_urls)}] Обработка: {url.split('/')[-1]}")
        
        img_url = extract_image_from_blogger_page(url)
        
        if img_url:
            # Получаем заголовок страницы для сопоставления
            # Повторно используем тот же объект soup? Нет, лучше сделать отдельный быстрый запрос или сохранить html
            # Для экономии времени и ресурсов: предположим, что имя файла в Hugo совпадает со slug в URL Blogger
            # Пример: .../2025/07/my-post-title.html -> my-post-title.md
            
            parsed = urlparse(url)
            path_parts = parsed.path.split('/')
            filename_with_ext = path_parts[-1] # my-post-title.html
            slug = filename_with_ext.replace('.html', '')
            
            image_map[slug] = img_url
            print(f"   ✅ SLUG: {slug} -> IMG: ...{img_url[-20:]}")
        else:
            print(f"   ℹ️ Картинка не найдена для {url}")
            
    return image_map

def update_markdown_files(image_map):
    """Обновляет .md файлы, заменяя поле image: на свежую ссылку из карты."""
    updated_count = 0
    
    for filename in os.listdir(CONTENT_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(CONTENT_DIR, filename)
        md_slug = filename[:-3] # Убираем .md
        
        print(f"\n📝 Проверка файла: {filename} (Slug: {md_slug})")
        
        fresh_url = image_map.get(md_slug)
        
        if not fresh_url:
            print("   -> ⚠️ Нет соответствия в карте Sitemap. Пропускаю.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Регулярка для замены поля image:
        pattern = r'(image:\s*)([^\n]+)'
        
        def replacer(match):
            prefix = match.group(1)
            old_val = match.group(2).strip()
            
            if old_val == fresh_url:
                return match.group(0) # Уже актуально
                
            print(f"   ✅ ЗАМЕНА:\n      OLD: {old_val}\n      NEW: {fresh_url}")
            return f'{prefix}{fresh_url}'
            
        new_content = re.sub(pattern, replacer, content, count=1)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            
    return updated_count

if __name__ == "__main__":
    # 1. Получаем список URL из Sitemap
    sitemap_urls = get_post_ids_from_sitemap()
    if not sitemap_urls:
        print("Критическая ошибка: Не удалось получить Sitemap.")
        sys.exit(1)
        
    # 2. Строим карту Slug -> ImageURL
    image_map = build_url_to_title_map(sitemap_urls)
    
    if not image_map:
        print("Предупреждение: Карта изображений пуста. Возможно, структура URL отличается.")
        sys.exit(0)
        
    # 3. Обновляем локальные Markdown файлы
    count = update_markdown_files(image_map)
    
    print(f"\n✨ Готово. Обновлено файлов: {count}")
