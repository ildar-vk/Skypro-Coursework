# tests/test_utils_for_views.py
import pytest
import pandas as pd
from datetime import datetime
from src.utils_for_views import (
    get_greeting,
    analyze_cards,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
    filter_transactions_by_month
)


class TestGetGreeting:
    """Тесты для функции get_greeting"""

    def test_get_greeting_returns_string(self):
        """Тест что функция возвращает строку"""
        result = get_greeting()
        assert isinstance(result, str)
        assert result in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


class TestAnalyzeCards:
    """Тесты для функции analyze_cards"""

    def test_analyze_cards_empty(self):
        """Тест с пустым списком транзакций"""
        result = analyze_cards([])
        assert result == []
        assert isinstance(result, list)

    def test_analyze_cards_with_expenses(self):
        """Тест с расходными операциями"""
        test_transactions = [
            {
                'Номер карты': '1234567890123456',
                'Сумма операции': -1000.0,
                'Категория': 'Супермаркет',
                'Описание': 'Покупки'
            },
            {
                'Номер карты': '1234567890123456',
                'Сумма операции': -500.0,
                'Категория': 'Кафе',
                'Описание': 'Обед'
            }
        ]

        result = analyze_cards(test_transactions)
        assert len(result) == 1
        assert result[0]['last_digits'] == '3456'
        assert result[0]['total_spent'] == 1500.0
        assert result[0]['cashback'] == 15.0


class TestGetTopTransactions:
    """Тесты для функции get_top_transactions"""

    def test_get_top_transactions_empty(self):
        """Тест с пустым списком транзакций"""
        result = get_top_transactions([])
        assert result == []
        assert isinstance(result, list)

    def test_get_top_transactions_with_missing_fields(self):
        """Тест топ транзакций с отсутствующими полями"""
        incomplete_transactions = [
            {'Сумма операции': -100},  # Нет даты
            {'Дата операции': '01.01.2023 12:00:00'},  # Нет суммы
        ]

        result = get_top_transactions(incomplete_transactions)
        assert isinstance(result, list)


class TestFilterTransactions:
    """Тесты для фильтрации транзакций"""

    def test_filter_transactions_by_month(self):
        """Тест фильтрации транзакций по месяцу"""
        test_transactions = [
            {
                'Дата операции': '15.01.2023 12:00:00',
                'Сумма операции': -100.0
            },
            {
                'Дата операции': '20.02.2023 12:00:00',
                'Сумма операции': -200.0
            }
        ]

        result = filter_transactions_by_month(test_transactions, "2023-02-28 23:59:59")
        assert len(result) == 1
        assert result[0]['Дата операции'] == '20.02.2023 12:00:00'


class TestCurrencyAndStocks:
    """Тесты для функций валют и акций"""

    def test_get_currency_rates(self):
        """Тест получения курсов валют"""
        result = get_currency_rates()
        assert isinstance(result, list)
        assert len(result) > 0

        # Проверяем структуру данных
        for currency in result:
            assert 'currency' in currency
            assert 'rate' in currency
            assert isinstance(currency['currency'], str)
            assert isinstance(currency['rate'], (int, float))

    def test_get_stock_prices(self):
        """Тест получения цен акций"""
        result = get_stock_prices()
        assert isinstance(result, list)
        assert len(result) > 0

        # Проверяем структуру данных
        for stock in result:
            assert 'stock' in stock
            assert 'price' in stock
            assert isinstance(stock['stock'], str)
            assert isinstance(stock['price'], (int, float))


class TestAPIFunctions:
    """Тесты для API функций"""

    def test_get_currency_rates_with_env_keys(self, monkeypatch):
        """Тест получения курсов валют с установленными ключами"""
        # Устанавливаем тестовые ключи
        monkeypatch.setenv('EXCHANGE_RATE_API_KEY', 'test_key_123')

        result = get_currency_rates()
        assert isinstance(result, list)
        assert len(result) > 0

        for currency in result:
            assert 'currency' in currency
            assert 'rate' in currency

    def test_get_stock_prices_with_env_keys(self, monkeypatch):
        """Тест получения цен акций с установленными ключами"""
        # Устанавливаем тестовые ключи
        monkeypatch.setenv('ALPHA_VANTAGE_API_KEY', 'test_key_456')

        result = get_stock_prices()
        assert isinstance(result, list)
        assert len(result) > 0

        for stock in result:
            assert 'stock' in stock
            assert 'price' in stock


class TestErrorCases:
    """Тесты для обработки ошибок"""

    def test_analyze_cards_with_invalid_data(self):
        """Тест анализа карт с некорректными данными"""
        invalid_transactions = [
            {'Номер карты': None, 'Сумма операции': -100},
            {'Номер карты': '', 'Сумма операции': -200},
        ]

        result = analyze_cards(invalid_transactions)
        assert isinstance(result, list)

    def test_filter_transactions_empty(self):
        """Тест фильтрации пустого списка транзакций"""
        result = filter_transactions_by_month([], "2023-02-28 23:59:59")
        assert result == []