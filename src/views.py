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
    logger.info(f"=== НАЧАЛО ФОРМИРОВАНИЯ ГЛАВНОЙ СТРАНИЦЫ ===")

    try:
        # 1. Загружаем данные
        df = process_bank_file(data_file)
        transactions = df.to_dict("records")
        logger.info(f"Загружено {len(transactions)} транзакций")

        # 2. ВРЕМЕННО: ИСПОЛЬЗУЕМ ВСЕ ТРАНЗАКЦИИ БЕЗ ФИЛЬТРАЦИИ
        filtered_transactions = transactions
        logger.info(f"ИСПОЛЬЗУЕМ ВСЕ {len(filtered_transactions)} ТРАНЗАКЦИЙ (фильтрация отключена)")

        # 3. Собираем компоненты
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
        logger.error(f"Ошибка: {e}")
        return {
            "greeting": get_greeting(),
            "cards": [],
            "top_transactions": [],
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }