# tests/test_utils.py
import pytest
import tempfile
import pandas as pd
from src.utils import process_bank_file, setup_logging, validate_file, read_excel_file


def test_setup_logging():
    """Тест настройки логирования"""
    # Просто проверяем что функция выполняется без ошибок
    try:
        setup_logging()
        assert True
    except Exception:
        assert False, "setup_logging вызвал исключение"


def test_validate_file_invalid_extension():
    """Тест валидации файла с неправильным расширением"""
    result = validate_file("test.txt")
    assert result is False


def test_validate_file_valid_extension():
    """Тест валидации файла с правильным расширением"""
    result = validate_file("test.xlsx")
    assert result is True


def test_process_bank_file_invalid_path():
    """Тест обработки несуществующего файла"""
    with pytest.raises(ValueError):  # Измените с FileNotFoundError на ValueError
        process_bank_file("non_existent_file.xlsx")


def test_read_excel_file_basic():
    """Базовый тест чтения Excel файла"""
    # Создаем временный Excel файл для теста
    test_data = pd.DataFrame({
        'Дата операции': ['01.01.2023 12:00:00'],
        'Сумма операции': [-100.0]
    })

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        test_data.to_excel(f.name, index=False)

        try:
            result = read_excel_file(f.name, 'openpyxl')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
        finally:
            import os
            os.unlink(f.name)