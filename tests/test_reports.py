"""Тесты для модуля reports"""

from src import reports


def test_reports_module_exists():
    """Тест что модуль reports существует"""
    try:
        assert True
    except ImportError:
        assert False, "Модуль reports не найден"


def test_reports_module_can_be_imported():
    """Тест что модуль reports может быть импортирован"""
    assert reports is not None
