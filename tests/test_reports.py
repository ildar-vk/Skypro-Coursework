"""Тесты для модуля reports"""


def test_reports_module_exists():
    """Тест что модуль reports существует"""
    try:
        import src.reports

        assert True
    except ImportError:
        assert False, "Модуль reports не найден"


def test_reports_module_can_be_imported():
    """Тест что модуль reports может быть импортирован"""
    from src import reports

    assert reports is not None
