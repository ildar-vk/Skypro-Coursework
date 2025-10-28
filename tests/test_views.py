# tests/test_views.py
import pytest
import sys
import os
from src.views import home_page
from src.utils import process_bank_file

class TestHomePage:
    """Тесты для главной страницы"""

    def test_home_page_returns_dict(self):
        """Тест что home_page возвращает словарь"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result, dict)

    def test_home_page_has_required_keys(self):
        """Тест что ответ содержит все обязательные ключи"""
        result = home_page("2024-01-15 14:30:00")

        required_keys = ['greeting', 'cards', 'top_transactions', 'currency_rates', 'stock_prices']
        for key in required_keys:
            assert key in result

    def test_home_page_greeting_is_string(self):
        """Тест что приветствие - строка"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result['greeting'], str)
        assert len(result['greeting']) > 0

    def test_home_page_cards_is_list(self):
        """Тест что cards - список"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result['cards'], list)

    def test_home_page_top_transactions_is_list(self):
        """Тест что top_transactions - список"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result['top_transactions'], list)

    def test_home_page_currency_rates_is_list(self):
        """Тест что currency_rates - список"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result['currency_rates'], list)
        assert len(result['currency_rates']) > 0

    def test_home_page_stock_prices_is_list(self):
        """Тест что stock_prices - список"""
        result = home_page("2024-01-15 14:30:00")
        assert isinstance(result['stock_prices'], list)
        assert len(result['stock_prices']) > 0

