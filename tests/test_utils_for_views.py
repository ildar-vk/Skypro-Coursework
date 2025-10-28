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

    def test_get_greeting_contains_keyword(self):
        """Тест что приветствие содержит ключевые слова"""
        result = get_greeting()
        assert any(word in result for word in ["Доброе", "Добрый", "Доброй"])


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
            },
            {
                'Номер карты': '9876543210987654',
                'Сумма операции': -200.0,
                'Категория': 'Транспорт',
                'Описание': 'Такси'
            }
        ]

        result = analyze_cards(test_transactions)

        assert len(result) == 2  # Две уникальные карты

        # Проверяем первую карту
        card1 = next(card for card in result if card['last_digits'] == '3456')
        assert card1['total_spent'] == 1500.0
        assert card1['cashback'] == 15.0

        # Проверяем вторую карту
        card2 = next(card for card in result if card['last_digits'] == '7654')
        assert card2['total_spent'] == 200.0
        assert card2['cashback'] == 2.0

    def test_analyze_cards_ignores_income(self):
        """Тест что функция игнорирует доходные операции (положительные суммы)"""
        test_transactions = [
            {
                'Номер карты': '1234567890123456',
                'Сумма операции': 1000.0,  # Положительная - пополнение
                'Категория': 'Пополнение',
                'Описание': 'Пополнение счета'
            },
            {
                'Номер карты': '1234567890123456',
                'Сумма операции': -500.0,  # Отрицательная - расход
                'Категория': 'Кафе',
                'Описание': 'Обед'
            }
        ]

        result = analyze_cards(test_transactions)

        # Должна быть только одна карта с одним расходом
        assert len(result) == 1
        assert result[0]['total_spent'] == 500.0
        assert result[0]['cashback'] == 5.0


class TestGetTopTransactions:
    """Тесты для функции get_top_transactions"""

    def test_get_top_transactions_empty(self):
        """Тест с пустым списком транзакций"""
        result = get_top_transactions([])
        assert result == []
        assert isinstance(result, list)

    def test_get_top_transactions_limit(self):
        """Тест ограничения количества возвращаемых транзакций"""
        test_transactions = [
            {'Сумма операции': -100, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'A', 'Описание': 'Test1'},
            {'Сумма операции': -200, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'B', 'Описание': 'Test2'},
            {'Сумма операции': -300, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'C', 'Описание': 'Test3'},
            {'Сумма операции': -400, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'D', 'Описание': 'Test4'},
            {'Сумма операции': -500, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'E', 'Описание': 'Test5'},
            {'Сумма операции': -600, 'Дата операции': '01.01.2023 12:00:00', 'Категория': 'F', 'Описание': 'Test6'},
        ]

        result = get_top_transactions(test_transactions, limit=3)
        assert len(result) == 3

        # Проверяем что вернулись самые крупные транзакции
        amounts = [t['amount'] for t in result]
        assert amounts == [-600, -500, -400]  # В порядке убывания

    def test_get_top_transactions_structure(self):
        """Тест структуры возвращаемых данных"""
        test_transactions = [
            {
                'Сумма операции': -1000.0,
                'Дата операции': '01.01.2023 12:00:00',
                'Категория': 'Супермаркет',
                'Описание': 'Покупки в магазине'
            }
        ]

        result = get_top_transactions(test_transactions)

        assert len(result) == 1
        transaction = result[0]

        assert 'date' in transaction
        assert 'amount' in transaction
        assert 'category' in transaction
        assert 'description' in transaction

        assert transaction['amount'] == -1000.0
        assert transaction['category'] == 'Супермаркет'


class TestCurrencyAndStocks:
    """Тесты для функций валют и акций"""

    def test_get_currency_rates(self):
        """Тест получения курсов валют"""
        result = get_currency_rates()

        assert isinstance(result, list)
        assert len(result) > 0

        for currency in result:
            assert 'currency' in currency
            assert 'rate' in currency
            assert isinstance(currency['rate'], float)

    def test_get_stock_prices(self):
        """Тест получения цен акций"""
        result = get_stock_prices()

        assert isinstance(result, list)
        assert len(result) > 0

        for stock in result:
            assert 'stock' in stock
            assert 'price' in stock
            assert isinstance(stock['price'], float)


class TestFilterTransactions:# не работает
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
            },
            {
                'Дата операции': '05.03.2023 12:00:00',
                'Сумма операции': -300.0
            }
        ]

        # Фильтруем до 28.02.2023 - должны получить только февраль
        result = filter_transactions_by_month(test_transactions, "2023-02-28 23:59:59")

        assert len(result) == 1
        dates = [t['Дата операции'] for t in result]
        assert '15.01.2023 12:00:00' not in dates
        assert '20.02.2023 12:00:00' in dates
        assert '05.03.2023 12:00:00' not in dates