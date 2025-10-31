"""
Модуль для работы с конфигурацией и API ключами.
"""

import os

from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Config:
    """Класс для хранения конфигурации API"""

    # API ключи - загружаем при создании класса
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

    # URL API
    ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
    EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/RUB"

    @classmethod
    def validate_keys(cls):
        """Проверяет наличие обязательных API ключей"""
        # Не перезагружаем dotenv, потому что monkeypatch уже подменил окружение
        alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        exchange_key = os.getenv("EXCHANGE_RATE_API_KEY")

        missing_keys = []
        if not alpha_key or alpha_key == "your_alpha_vantage_key_here":
            missing_keys.append("ALPHA_VANTAGE_API_KEY")
        if not exchange_key or exchange_key == "your_exchange_rate_key_here":
            missing_keys.append("EXCHANGE_RATE_API_KEY")

        if missing_keys:
            print(f"⚠️  Предупреждение: Отсутствуют API ключи: {', '.join(missing_keys)}")
            print("💡 Используются заглушки. Для реальных данных получите ключи:")
            print("   - Alpha Vantage: https://www.alphavantage.co/support/#api-key")
            print("   - ExchangeRate: https://app.exchangerate-api.com/sign-up")
        return len(missing_keys) == 0
