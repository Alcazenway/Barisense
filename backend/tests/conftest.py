import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.dependencies import get_repository
from app.main import app
from app.services.repository import Repository


@pytest.fixture
def client():
    repository = Repository()
    app.dependency_overrides[get_repository] = lambda: repository
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_api_key_env():
    prev = os.environ.pop("BARISENSE_API_KEY", None)
    get_settings.cache_clear()
    yield
    if prev:
        os.environ["BARISENSE_API_KEY"] = prev
    get_settings.cache_clear()
