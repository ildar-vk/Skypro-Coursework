"""
Модуль views - содержит основные функции для генерации JSON ответов.
Соответствует принципу "тонкие views, толстые модели".
"""
import logging
from typing import Dict, Any, List

from utils_for_views import (
    get_greeting,
    filter_transactions_by_month,
    analyze_cards,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices
)
from utils import process_bank_file

logger = logging.getLogger(__name__)


def home_page(target_date: str, data_file: str = "data/operations.xlsx") -> Dict[str, Any]:
    """
    Генерирует JSON-данные для главной страницы.

    Args:
        target_date: Дата в формате 'YYYY-MM-DD HH:MM:SS'
        data_file: Путь к файлу с транзакциями

    Returns:
        Словарь с данными для JSON-ответа
    """
    logger.info(f"Начало формирования главной страницы для даты: {target_date}")

    try:
        # 1. Загружаем данные
        df = process_bank_file(data_file)
        transactions = df.to_dict("records")

        # 2. Фильтруем данные по месяцу
        filtered_transactions = filter_transactions_by_month(transactions, target_date)

        # 3. Собираем все компоненты (делегируем работу хелперам)
        result = {
            "greeting": get_greeting(),
            "cards": analyze_cards(filtered_transactions),
            "top_transactions": get_top_transactions(filtered_transactions),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }

        logger.info("Главная страница успешно сформирована")
        return result

    except Exception as e:
        logger.error(f"Критическая ошибка в home_page: {e}")
        # Возвращаем базовую структуру при ошибке
        return {
            "greeting": get_greeting(),
            "cards": [],
            "top_transactions": [],
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }