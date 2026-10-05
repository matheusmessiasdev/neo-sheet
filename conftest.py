# conftest.py
import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def clear_cache_between_tests():
    """
    Limpa o cache antes e depois de cada teste, evitando que respostas
    cacheadas vazem entre testes.
    """
    cache.clear()
    yield
    cache.clear()
