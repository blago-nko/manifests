"""Unit-тесты для scripts/check_docs_links.py (INFRA-036)."""
import subprocess
import sys
from pathlib import Path


def test_check_docs_links_passes():
    """check_docs_links.py должен проходить без ошибок (все внутренние ссылки валидны)."""
    result = subprocess.run(
        [sys.executable, 'scripts/check_docs_links.py'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0, f'STDERR: {result.stderr}\nSTDOUT: {result.stdout}'
    assert 'links OK' in result.stdout
