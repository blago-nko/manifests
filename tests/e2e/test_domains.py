"""E2E-тесты для 14 доменов экосистемы (INFRA-036)."""
import pytest
from playwright.sync_api import sync_playwright


DOMAINS = [
    ('https://blagorussia.ru', 'blagorussia.ru'),
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


@pytest.mark.parametrize('url,name', DOMAINS, ids=[d[1] for d in DOMAINS])
def test_domain_returns_200(url, name):
    """Каждый домен должен возвращать HTTP 200."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = page.goto(url, timeout=30000)
        assert response is not None, f'{name}: нет ответа'
        assert response.status == 200, f'{name}: статус {response.status}'
        browser.close()


@pytest.mark.parametrize('url,name', DOMAINS, ids=[d[1] for d in DOMAINS])
def test_domain_has_content(url, name):
    """Каждый домен должен содержать контент (body не пустой)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        body = page.locator('body')
        assert body.count() > 0, f'{name}: body отсутствует'
        browser.close()
