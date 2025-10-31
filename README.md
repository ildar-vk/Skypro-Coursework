# Анализ банковских операций

Проект для анализа банковских операций, загружаемых из Excel-файла.

## Функциональность

- Загрузка данных из Excel-файла
- Анализ расходов по картам
- Определение топовых транзакций
- Отображение курсов валют и акций
- Формирование JSON-отчета для главной страницы

## Установка

# Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd Courcework
# Установите зависимости с помощью Poetry:
    poetry install
# Активируйте виртуальное окружение:
    poetry shell
# Запустите главный скрипт:
    poetry run python src/main.py

## PEP8 и кодстайл

# Установи если нет
pip install autopep8 flake8 black

# Автоисправление стиля
autopep8 --in-place --aggressive --recursive src/

# Или black (более строгий)
black src/

# Проверка без исправлений
flake8 src/

##  Настройка API

Проект поддерживает получение реальных данных через API:

### Получение API ключей (бесплатно):

1. **Акции S&P500**:
   - Зарегистрируйтесь на [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Получите бесплатный API ключ

2. **Курсы валют**:
   - Зарегистрируйтесь на [ExchangeRate-API](https://app.exchangerate-api.com/sign-up)
   - Получите бесплатный API ключ

### Настройка:

1. Скопируйте `.env_template` в `.env`
2. Заполните реальными API ключами:

ALPHA_VANTAGE_API_KEY=ваш_ключ_здесь
EXCHANGE_RATE_API_KEY=ваш_ключ_здесь

## Проверка что всё работает

# Запускаем основной код
poetry run python src/main.py

# Запускаем тесты
poetry run pytest tests/ -v

# Проверяем покрытие
poetry run pytest --cov=src --cov-report=term-missing tests/