# tests/test_utils.py
import pytest
import pandas as pd
import os
from src.utils import process_bank_file, setup_logging


class TestUtils:
    """Тесты для утилит"""

    def test_setup_logging(self):
        """Тест настройки логирования"""
        # Просто проверяем что функция выполняется без ошибок
        try:
            setup_logging()
            assert True
        except Exception:
            assert False, "setup_logging вызвал исключение"

    def test_process_bank_file_exists(self, tmp_path):
        """Тест обработки банковского файла"""
        # Создаем временный Excel файл для теста
        test_data = {
            'Дата операции': ['01.01.2023 12:00:00', '02.01.2023 12:00:00'],
            'Номер карты': ['1234567890123456', '1234567890123456'],
            'Сумма операции': [-100.0, -200.0],
            'Категория': ['Супермаркет', 'Кафе'],
            'Описание': ['Покупки', 'Обед']
        }
        df = pd.DataFrame(test_data)

        test_file = tmp_path / "test_operations.xlsx"
        df.to_excel(test_file, index=False)

        # Обрабатываем файл
        result = process_bank_file(str(test_file))

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'Дата операции' in result.columns