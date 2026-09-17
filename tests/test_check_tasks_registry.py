"""Unit-тесты для scripts/check_tasks_registry.py (INFRA-036)."""
import subprocess
import sys
from pathlib import Path


def test_check_tasks_registry_passes():
    """check_tasks_registry.py должен проходить без ошибок на чистом TASKS.md."""
    result = subprocess.run(
        [sys.executable, 'scripts/check_tasks_registry.py'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0, f'STDERR: {result.stderr}\nSTDOUT: {result.stdout}'
    assert 'tasks registry OK' in result.stdout
