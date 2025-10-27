"""
Вспомогательные функции для views.
Содержит бизнес-логику для формирования данных веб-страниц.
"""
import logging
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


def get_greeting() -> str:
    """
    Определяет приветствие в зависимости от времени суток.
    """
    try:
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            return "Доброе утро"
        elif 12 <= current_hour < 18:
            return "Добрый день"
        elif 18 <= current_hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except Exception as e:
        logger.warning(f"{__name__}.[get_greeting] Ошибка определения времени: {e}")
        return "Добро пожаловать"


def filter_transactions_by_month(transactions: List[Dict], target_date: str) -> List[Dict]:
    """
    Фильтрует транзакции по месяцу указанной даты.
    Работает со списком словарей вместо DataFrame.
    """
    try:
        target_dt = pd.to_datetime(target_date.split()[0])
        month_start = target_dt.replace(day=1)

        filtered = []
        for transaction in transactions:
            op_date = pd.to_datetime(transaction['Дата операции'])
            if month_start <= op_date <= target_dt:
                filtered.append(transaction)

        logger.info(f"{__name__}.[filter_transactions_by_month] Отфильтровано {len(filtered)} из {len(transactions)} транзакций")
        return filtered

    except Exception as e:
        logger.error(f"{__name__}.[filter_transactions_by_month] Ошибка фильтрации транзакций: {e}")
        return transactions


def analyze_cards(transactions: List[Dict]) -> List[Dict[str, Any]]:
    """
    Анализирует расходы по картам из списка транзакций.
    """
    cards_data = []

    try:
        # Берем только расходы (отрицательные суммы)
        expenses = [t for t in transactions if t['Сумма операции'] < 0]

        # Группируем по номерам карт
        cards = set()
        for expense in expenses:
            card = expense.get('Номер карты')
            if card and not pd.isna(card):
                cards.add(card)

        for card in cards:
            card_expenses = [e for e in expenses if e.get('Номер карты') == card]
            total_spent = abs(sum(e['Сумма операции'] for e in card_expenses))
            cashback = total_spent * 0.01

            cards_data.append({
                "last_digits": str(card)[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

        logger.info(f"{__name__}.[analyze_cards] Проанализировано {len(cards_data)} карт")

    except Exception as e:
        logger.error(f"Ошибка анализа карт: {e}")

    return cards_data


def get_top_transactions(transactions: List[Dict], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Находит топ транзакций по сумме платежа (только расходы) из списка транзакций.
    """
    try:
        logger.info(f"{__name__}.[get_top_transactions] Поиск топ {limit} транзакций (расходы) из {len(transactions)}")

        # Фильтруем только расходы (отрицательные суммы)
        expenses = [t for t in transactions if t.get('Сумма операции', 0) < 0]
        logger.info(f"Найдено {len(expenses)} расходных операций")

        # Сортируем по абсолютной сумме (по убыванию)
        sorted_expenses = sorted(
            expenses,
            key=lambda x: abs(x.get('Сумма операции', 0)),
            reverse=True
        )

        top_transactions = []
        for transaction in sorted_expenses[:limit]:
            op_date = transaction['Дата операции']
            if isinstance(op_date, str):
                date_str = op_date.split()[0]  # Берем только дату
            else:
                date_str = str(op_date).split()[0]

            amount = transaction.get('Сумма операции', 0)
            category = transaction.get('Категория', 'Не указана')

            # Заменяем nan на "Не указана"
            if pd.isna(category):
                category = "Не указана"

            top_transactions.append({
                "date": date_str,
                "amount": round(amount, 2),
                "category": category,
                "description": transaction.get('Описание', 'Без описания')
            })

        logger.info(f"{__name__}.[get_top_transactions] Найдено {len(top_transactions)} топ транзакций (расходы)")
        return top_transactions

    except Exception as e:
        logger.error(f"Ошибка получения топ транзакций: {e}")
        return []

def get_currency_rates() -> List[Dict[str, Any]]:
    """
    Получает курсы валют (заглушка).
    """
    # TODO: Реализовать через API
    return [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 85.0}
    ]


def get_stock_prices() -> List[Dict[str, Any]]:
    """
    Получает цены акций (заглушка).
    """
    # TODO: Реализовать через API
    return [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3200.0},
        {"stock": "GOOGL", "price": 2800.0}
    ]