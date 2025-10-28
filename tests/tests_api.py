import pytest
from unittest.mock import patch, Mock
from src.utils_for_views import get_currency_rates, get_stock_prices


@patch('src.utils_for_views.requests.get')
def test_get_currency_rates_api_success(mock_get):
    """Тест успешного получения курсов валют через API"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'rates': {'USD': 75.5, 'EUR': 85.2, 'GBP': 95.1}
    }
    mock_get.return_value = mock_response

    result = get_currency_rates()
    assert len(result) > 0
    assert result[0]['currency'] == 'USD'


@patch('src.utils_for_views.requests.get')
def test_get_currency_rates_api_failure(mock_get):
    """Тест обработки ошибки API курсов валют"""
    mock_get.side_effect = Exception("API error")

    result = get_currency_rates()
    # Должен вернуть заглушку при ошибке
    assert len(result) > 0
    assert result[0]['currency'] == 'USD'