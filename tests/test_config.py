"""
Простые тесты для конфигурации.
"""

from src.config import Config


def test_config_attributes_exist():
    """Тест что у Config есть нужные атрибуты"""
    assert hasattr(Config, "ALPHA_VANTAGE_API_KEY")
    assert hasattr(Config, "EXCHANGE_RATE_API_KEY")
    assert hasattr(Config, "ALPHA_VANTAGE_URL")
    assert hasattr(Config, "EXCHANGE_RATE_URL")


def test_config_validate_keys_without_keys(monkeypatch):
    """Тест проверки ключей когда ключей нет"""
    # Временно убираем ключи из окружения
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "")
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "")

    # Должен вернуть False когда ключей нет
    assert Config.validate_keys() == False


def test_config_validate_keys_with_template_keys(monkeypatch):
    """Тест проверки ключей когда ключи шаблонные"""
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "your_alpha_vantage_key_here")
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "your_exchange_rate_key_here")

    assert Config.validate_keys() == False


def test_config_validate_keys_with_real_keys(monkeypatch):
    """Тест проверки ключей когда ключи настоящие"""
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "real_key_123")
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "real_key_456")

    assert Config.validate_keys() == True


def test_config_validate_keys_message(monkeypatch, capsys):
    """Тест что при отсутствии ключей выводится сообщение"""
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "")
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "")

    Config.validate_keys()
    captured = capsys.readouterr()

    # Проверяем что выводится предупреждение
    assert "Отсутствуют API ключи" in captured.out
    assert "Alpha Vantage" in captured.out
