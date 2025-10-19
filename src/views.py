"""Генерация JSON данных для веб-страниц."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests


"""
Веб-страницы - генерация JSON для фронтенда.
"""
import logging
from datetime import datetime
from typing import Dict, Any, List

import pandas as pd

# Настраиваем логирование
logger = logging.getLogger(__name__)


def home_page(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Главная страница - генерирует JSON данные для веб-интерфейса.

    Args:
        df: DataFrame с транзакциями (УЖЕ прочитан!)

    Returns:
        JSON структура для главной страницы
    """
    try:
        logger.info("Генерация главной страницы...")

        # Импортируем утилиты
        from utils import get_latest_transaction_date, get_recent_transactions

        # 1. Получаем актуальные данные
        latest_date = get_latest_transaction_date(df)
        recent_transactions = get_recent_transactions(df, days=30, limit=5)

        # 2. Фильтруем данные за последний месяц
        latest_dt = pd.to_datetime(latest_date)
        month_start = latest_dt.replace(day=1)
        monthly_mask = (df['Дата операции'] >= month_start) & (df['Дата операции'] <= latest_dt)
        monthly_df = df[monthly_mask]

        # 3. Собираем JSON
        result = {
            "analysis_info": {
                "latest_transaction_date": latest_date,
                "analysis_period": f"{month_start.strftime('%d.%m.%Y')} - {latest_dt.strftime('%d.%m.%Y')}",
                "total_transactions_analyzed": len(monthly_df)
            },
            "greeting": _get_greeting(latest_date),
            "cards": _analyze_cards(monthly_df),
            "recent_transactions": recent_transactions,
            "top_transactions": _get_top_transactions(monthly_df),
            "currency_rates": _get_currency_rates(),
            "stock_prices": _get_stock_prices(),
        }

        logger.info("Главная страница успешно сгенерирована")
        return result

    except Exception as e:
        logger.error(f"Ошибка генерации главной страницы: {e}")
        return {"error": str(e)}


def _get_greeting(date_str: str) -> str:
    """
    Возвращает приветствие по времени суток.

    Args:
        date_str: Дата для анализа времени

    Returns:
        Приветствие
    """
    try:
        # Пока упрощенная версия - всегда "Добрый день"
        return "Добрый день"
    except Exception:
        return "Добрый день"


def _analyze_cards(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Анализирует расходы по картам.

    Args:
        df: DataFrame с транзакциями

    Returns:
        Список данных по картам
    """
    try:
        cards_data = []

        # Берем только расходы
        expenses = df[df['Сумма операции'] < 0]

        for card in expenses['Номер карты'].unique():
            if pd.isna(card):
                continue

            card_data = expenses[expenses['Номер карты'] == card]
            total_spent = abs(card_data['Сумма операции'].sum())
            cashback = total_spent * 0.01  # 1% кешбэк

            cards_data.append({
                "last_digits": str(card)[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

        logger.info(f"Проанализировано {len(cards_data)} карт")
        return cards_data

    except Exception as e:
        logger.error(f"Ошибка анализа карт: {e}")
        return []


def _get_top_transactions(df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Находит топ операций по абсолютной сумме.

    Args:
        df: DataFrame с транзакциями
        limit: Количество операций для возврата

    Returns:
        Список топ операций
    """
    try:
        # Сортируем по абсолютному значению
        df_temp = df.copy()
        df_temp['abs_amount'] = df_temp['Сумма операции'].abs()
        top_df = df_temp.nlargest(limit, 'abs_amount')

        transactions = []
        for _, row in top_df.iterrows():
            transactions.append({
                "date": row['Дата операции'].strftime('%d.%m.%Y'),
                "amount": round(row['Сумма операции'], 2),
                "category": row.get('Категория', 'Неизвестно'),
                "description": row.get('Описание', 'Без описания')
            })

        logger.info(f"Найдено {len(transactions)} топ операций")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка поиска топ операций: {e}")
        return []


def _get_currency_rates() -> List[Dict[str, Any]]:
    """
    Возвращает курсы валют (заглушка).

    Returns:
        Список курсов валют
    """
    # Заглушка - в реальном приложении здесь будет API
    return [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 85.0}
    ]


def _get_stock_prices() -> List[Dict[str, Any]]:
    """
    Возвращает цены акций (заглушка).

    Returns:
        Список цен акций
    """
    # Заглушка - в реальном приложении здесь будет API
    return [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "GOOGL", "price": 2700.0}
    ]