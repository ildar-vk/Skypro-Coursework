import logging
import os
import sys
from typing import Any, Dict

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(__file__))

# Универсальные импорты
try:
    # Для запуска из корня проекта (тесты)
    from utils import process_bank_file
    from utils_for_views import (
        analyze_cards,
        filter_transactions_by_month,
        get_currency_rates,
        get_greeting,
        get_stock_prices,
        get_top_transactions,
    )
except ImportError:
    # Для запуска из папки src (основное приложение)
    from .utils import process_bank_file
    from .utils_for_views import (
        analyze_cards,
        filter_transactions_by_month,
        get_currency_rates,
        get_greeting,
        get_stock_prices,
        get_top_transactions,
    )

logger = logging.getLogger(__name__)


def home_page(target_date: str, data_file: str = "data/operations.xlsx") -> Dict[str, Any]:
    logger.info("=== НАЧАЛО ФОРМИРОВАНИЯ ГЛАВНОЙ СТРАНИЦЫ ===")

    try:
        # Загружаем данные
        df = process_bank_file(data_file)
        transactions = df.to_dict("records")
        logger.info(f"Загружено {len(transactions)} транзакций")

        # filtered_transactions = transactions
        # logger.info(f"ИСПОЛЬЗУЕМ ВСЕ {len(filtered_transactions)} ТРАНЗАКЦИЙ (фильтрация отключена)")
        filtered_transactions = filter_transactions_by_month(transactions, target_date)
        logger.info(f"Отфильтровано {len(filtered_transactions)} транзакций за период до {target_date}")
        # Собираем компоненты
        result = {
            "greeting": get_greeting(),
            "cards": analyze_cards(filtered_transactions),
            "top_transactions": get_top_transactions(filtered_transactions),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices(),
        }

        logger.info(f"{__name__}.[home_page] Главная страница успешно сформирована")
        return result

    except Exception as e:
        logger.error(f"{__name__}.[home_page] Ошибка: {e}")
        return {
            "greeting": get_greeting(),
            "cards": [],
            "top_transactions": [],
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices(),
        }
