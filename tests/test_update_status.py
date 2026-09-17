"""Unit-тесты для scripts/update_status.py (INFRA-036)."""
import subprocess
import sys
from pathlib import Path


def test_update_status_runs_without_error():
    """Скрипт update_status.py должен выполняться без ошибок."""
    result = subprocess.run(
        [sys.executable, 'scripts/update_status.py'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0, f'STDERR: {result.stderr}'
    assert 'STATUS.md обновлён' in result.stdout


def test_status_md_exists_after_update():
    """После выполнения update_status.py docs/STATUS.md должен существовать."""
    subprocess.run(
        [sys.executable, 'scripts/update_status.py'],
        check=True,
        cwd=Path(__file__).parent.parent,
    )
    status_path = Path(__file__).parent.parent / 'docs' / 'STATUS.md'
    assert status_path.exists(), 'docs/STATUS.md не создан'
    content = status_path.read_text(encoding='utf-8')
    assert '# 📈 Статус документов' in content


def test_status_md_contains_required_sections():
    """docs/STATUS.md должен содержать обязательные секции."""
    subprocess.run(
        [sys.executable, 'scripts/update_status.py'],
        check=True,
        cwd=Path(__file__).parent.parent,
    )
    status_path = Path(__file__).parent.parent / 'docs' / 'STATUS.md'
    content = status_path.read_text(encoding='utf-8')
    required = [
        '## Текущее состояние',
        '## Состояние манифестов',
        '## Состояние 14 доменов',
        '## Ключевые метрики',
    ]
    for section in required:
        assert section in content, f"Секция '{section}' отсутствует в STATUS.md"
