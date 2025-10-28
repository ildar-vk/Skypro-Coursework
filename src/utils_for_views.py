"""
Вспомогательные функции для views.
Содержит бизнес-логику для формирования данных веб-страниц.
"""

import logging
import requests
from datetime import datetime
from typing import Any, Dict, List
from config import Config

import pandas as pd

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
    """Фильтрует список транзакций по месяцу"""
    try:
        if not transactions:
            logger.warning("Получен пустой список транзакций для фильтрации")
            return []

        # Парсим целевую дату
        target_dt = pd.to_datetime(target_date, format='%Y-%m-%d %H:%M:%S')

        # Для отладки - посмотрим на первые несколько дат в данных
        sample_dates = []
        for i, t in enumerate(transactions[:5]):
            if 'Дата операции' in t:
                sample_dates.append(t['Дата операции'])
        logger.info(f"Пример дат в данных: {sample_dates}")
        logger.info(f"Целевая дата фильтрации: {target_dt}")

        filtered = []
        skipped_count = 0

        for transaction in transactions:
            try:
                op_date_str = transaction.get('Дата операции')
                if not op_date_str or pd.isna(op_date_str):
                    skipped_count += 1
                    continue

                # Парсим дату операции (формат: 'дд.мм.гггг чч:мм:сс')
                op_date = pd.to_datetime(op_date_str, format='%d.%m.%Y %H:%M:%S')

                # Проверяем, что дата операции в том же году и месяце, что и целевая
                if op_date.year == target_dt.year and op_date.month == target_dt.month:
                    filtered.append(transaction)

            except Exception as e:
                logger.warning(f"Ошибка парсинга даты '{op_date_str}': {e}")
                skipped_count += 1
                continue

        logger.info(
            f"Отфильтровано {len(filtered)} транзакций за {target_dt.month}.{target_dt.year}, пропущено {skipped_count}")
        return filtered

    except Exception as e:
        logger.error(f"Критическая ошибка в filter_transactions_by_month: {e}")
        # В случае ошибки возвращаем все транзакции как fallback
        return transactions


def analyze_cards(transactions: List[Dict]) -> List[Dict[str, Any]]:
    """
    Анализирует расходы по картам из списка транзакций.
    """
    cards_data = []

    try:
        # Берем только расходы (отрицательные суммы)
        expenses = [t for t in transactions if t["Сумма операции"] < 0]

        # Группируем по номерам карт
        cards = set()
        for expense in expenses:
            card = expense.get("Номер карты")
            if card and not pd.isna(card):
                cards.add(card)

        for card in cards:
            card_expenses = [e for e in expenses if e.get("Номер карты") == card]
            total_spent = abs(sum(e["Сумма операции"] for e in card_expenses))
            cashback = total_spent * 0.01

            cards_data.append(
                {"last_digits": str(card)[-4:], "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)}
            )

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
        expenses = [t for t in transactions if t.get("Сумма операции", 0) < 0]
        logger.info(f"Найдено {len(expenses)} расходных операций")

        # Сортируем по абсолютной сумме (по убыванию)
        sorted_expenses = sorted(expenses, key=lambda x: abs(x.get("Сумма операции", 0)), reverse=True)

        top_transactions = []
        for transaction in sorted_expenses[:limit]:
            op_date = transaction["Дата операции"]
            if isinstance(op_date, str):
                date_str = op_date.split()[0]  # Берем только дату
            else:
                date_str = str(op_date).split()[0]

            amount = transaction.get("Сумма операции", 0)
            category = transaction.get("Категория", "Не указана")

            # Заменяем nan на "Не указана"
            if pd.isna(category):
                category = "Не указана"

            top_transactions.append(
                {
                    "date": date_str,
                    "amount": round(amount, 2),
                    "category": category,
                    "description": transaction.get("Описание", "Без описания"),
                }
            )

        logger.info(f"{__name__}.[get_top_transactions] Найдено {len(top_transactions)} топ транзакций (расходы)")
        return top_transactions

    except Exception as e:
        logger.error(f"Ошибка получения топ транзакций: {e}")
        return []


def get_currency_rates() -> List[Dict[str, Any]]:
    """
    Получает реальные курсы валют через API.
    Если API недоступно, возвращает заглушку.
    """
    try:
        # Проверяем наличие API ключа
        if not Config.EXCHANGE_RATE_API_KEY:
            logger.warning("API ключ для курсов валют не найден, используем заглушку")
            return get_currency_rates_stub()

        # Делаем реальный запрос к API
        response = requests.get(Config.EXCHANGE_RATE_URL, timeout=10)

        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})

            # Возвращаем курсы для основных валют
            return [
                {"currency": "USD", "rate": round(rates.get('USD', 75.0), 2)},
                {"currency": "EUR", "rate": round(rates.get('EUR', 85.0), 2)},
                {"currency": "GBP", "rate": round(rates.get('GBP', 95.0), 2)},
            ]
        else:
            logger.warning(f"Ошибка API курсов валют: {response.status_code}")
            return get_currency_rates_stub()

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return get_currency_rates_stub()


def get_currency_rates_stub() -> List[Dict[str, Any]]:
    """Заглушка для курсов валют"""
    return [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 85.0}
    ]


def get_stock_prices() -> List[Dict[str, Any]]:
    """
    Получает реальные цены акций через Alpha Vantage API.
    Если API недоступно, возвращает заглушку.
    """
    try:
        # Проверяем наличие API ключа
        if not Config.ALPHA_VANTAGE_API_KEY:
            logger.warning("API ключ для акций не найден, используем заглушку")
            return get_stock_prices_stub()

        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        stock_prices = []

        for symbol in stocks:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': Config.ALPHA_VANTAGE_API_KEY
            }

            response = requests.get(Config.ALPHA_VANTAGE_URL, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                quote = data.get('Global Quote', {})
                price = float(quote.get('05. price', 0))

                if price > 0:
                    stock_prices.append({
                        "stock": symbol,
                        "price": round(price, 2)
                    })
            else:
                logger.warning(f"Ошибка API для акции {symbol}: {response.status_code}")

        # Если получили хотя бы некоторые данные, возвращаем их
        if stock_prices:
            return stock_prices
        else:
            return get_stock_prices_stub()

    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        return get_stock_prices_stub()


def get_stock_prices_stub() -> List[Dict[str, Any]]:
    """Заглушка для цен акций"""
    return [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3200.0},
        {"stock": "GOOGL", "price": 2800.0}
    ]
