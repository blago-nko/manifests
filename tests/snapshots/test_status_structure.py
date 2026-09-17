"""Snapshot-тесты для структуры docs/STATUS.md (INFRA-036)."""
import re
from pathlib import Path


def test_status_md_structure():
    """Проверка структуры docs/STATUS.md (обязательные секции и формат)."""
    status_path = Path(__file__).parent.parent.parent / 'docs' / 'STATUS.md'
    content = status_path.read_text(encoding='utf-8')

    # Проверка заголовка
    assert content.startswith('# 📈 Статус документов'), 'Неверный заголовок'

    # Проверка обязательных секций
    required_sections = [
        '## Текущее состояние',
        '## Состояние манифестов',
        '## Состояние 14 доменов',
        '## Ключевые метрики',
    ]
    for section in required_sections:
        assert section in content, f"Секция '{section}' отсутствует"

    # Проверка таблицы манифестов
    assert '| Манифест |' in content, 'Таблица манифестов отсутствует'

    # Проверка timestamp
    timestamp_pattern = r'\d{4}-\d{2}-\d{2}'
    assert re.search(timestamp_pattern, content), 'Timestamp отсутствует или неверный формат'
