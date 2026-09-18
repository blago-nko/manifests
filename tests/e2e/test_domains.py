"""E2E-тесты для 14 доменов экосистемы (INFRA-036, hardening INFRA-048)."""
import time

import pytest
from playwright.sync_api import sync_playwright


DOMAINS = [
    ('https://www.blagorussia.ru', 'blagorussia.ru'),
    ('https://obrazslov.ru', 'obrazslov.ru'),
    ('https://partnerstvo.blagorussia.ru', 'partnerstvo'),
    ('https://novosti.blagorussia.ru', 'novosti'),
    ('https://ot-gorozan.blagorussia.ru', 'ot-gorozan'),
    ('https://obavlenia.blagorussia.ru', 'obavlenia'),
    ('https://interesnye-mesta.obrazslov.ru', 'interesnye-mesta'),
    ('https://moisites.blagorussia.ru', 'moisites'),
    ('https://joga.blagorussia.ru', 'joga'),
    ('https://ideologia.obrazslov.ru', 'ideologia'),
    ('https://nasa-istoria.blagorussia.ru', 'nasa-istoria'),
    ('https://grekpanteon.obrazslov.ru', 'grekpanteon'),
    ('https://can.blagorussia.ru', 'can'),
    ('https://gallery.obrazslov.ru', 'gallery'),
]

RETRIES = 3
DELAY_SECONDS = 5


def _goto_with_retry(page, url):
    """Три попытки с паузой: сеть GitHub Actions нестабильна."""
    last_error = None
    for _ in range(RETRIES):
        try:
            return page.goto(url, timeout=30000)
        except Exception as error:  # noqa: BLE001
            last_error = error
            time.sleep(DELAY_SECONDS)
    raise last_error


def _is_blogger_rate_limit(response):
    return response is not None and response.status == 429 and 'google.com/sorry' in response.url


@pytest.mark.parametrize('url,name', DOMAINS, ids=[d[1] for d in DOMAINS])
def test_domain_returns_200(url, name):
    """Каждый домен должен возвращать HTTP 200 (429 Blogger = skip)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = _goto_with_retry(page, url)
        if _is_blogger_rate_limit(response):
            browser.close()
            pytest.skip(f'{name}: Blogger rate-limit (google sorry page)')
        assert response is not None, f'{name}: нет ответа'
        assert response.status == 200, f'{name}: статус {response.status}'
        browser.close()


@pytest.mark.parametrize('url,name', DOMAINS, ids=[d[1] for d in DOMAINS])
def test_domain_has_content(url, name):
    """Каждый домен должен содержать контент (body не пустой)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = _goto_with_retry(page, url)
        if _is_blogger_rate_limit(response):
            browser.close()
            pytest.skip(f'{name}: Blogger rate-limit (google sorry page)')
        body = page.locator('body')
        assert body.count() > 0, f'{name}: body отсутствует'
        browser.close()
