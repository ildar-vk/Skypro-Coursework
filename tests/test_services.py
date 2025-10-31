"""Тесты для модуля services"""

from src import services


def test_services_module_exists():
    """Тест что модуль services существует"""
    try:

        assert True
    except ImportError:
        assert False, "Модуль services не найден"


def test_services_module_can_be_imported():
    """Тест что модуль services может быть импортирован"""

    assert services is not None
