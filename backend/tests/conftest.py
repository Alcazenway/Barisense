import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.dependencies import get_repository


@pytest.fixture(autouse=True)
def reset_repository() -> None:
    """Ensure each test runs with a fresh in-memory repository."""
    get_repository.cache_clear()
    yield
    get_repository.cache_clear()
