# src/main.py
import json
import logging
from views import home_page
from utils import process_bank_file, setup_logging


def main():
    """Главная функция для тестирования ВСЕГО проекта."""
    setup_logging()
    logger = logging.getLogger(__name__)

    print("🚀 Запуск тестирования проекта 'Анализ банковских операций'")
    print("=" * 60)

    try:
        # ТЕСТ 1: Загрузка данных (твой оригинальный код)
        print("\n📊 ТЕСТ 1: Загрузка данных из Excel...")
        file_path = "data/operations.xlsx"
        df = process_bank_file(file_path)
        print(f"✅ Готово! Загружено {len(df)} транзакций")

        # Показываем немного информации о данных
        print(f"   • Колонки: {list(df.columns)}")
        print(f"   • Диапазон дат: от {df['Дата операции'].min()} до {df['Дата операции'].max()}")

        # ТЕСТ 2: Главная страница (новая функциональность)
        print("\n🌐 ТЕСТ 2: Генерация главной страницы...")
        test_date = "2024-01-15 14:30:00"
        result = home_page(test_date, file_path)

        print("✅ Главная страница сгенерирована успешно!")
        print(f"   • Приветствие: {result['greeting']}")
        print(f"   • Карт проанализировано: {len(result['cards'])}")
        print(f"   • Топ транзакций: {len(result['top_transactions'])}")
        print(f"   • Курсов валют: {len(result['currency_rates'])}")
        print(f"   • Акций: {len(result['stock_prices'])}")

        # Сохраняем полный результат в файл
        with open('home_page_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("💾 Полный результат сохранен в 'home_page_result.json'")

        # ТЕСТ 3: Показываем пример данных
        print("\n📋 ТЕСТ 3: Пример данных из результата:")
        if result['cards']:
            print("\n💳 Данные по картам:")
            for card in result['cards'][:2]:  # Показываем первые 2 карты
                print(f"   • Карта ...{card['last_digits']}:")
                print(f"     Потрачено: {card['total_spent']} руб")
                print(f"     Кешбэк: {card['cashback']} руб")

        if result['top_transactions']:
            print("\n📈 Топ транзакции:")
            for i, transaction in enumerate(result['top_transactions'][:3], 1):  # Первые 3
                print(f"   {i}. {transaction['date']} - {transaction['amount']} руб")
                print(f"      Категория: {transaction['category']}")
                desc = transaction['description']
                print(f"      Описание: {desc[:50]}{'...' if len(desc) > 50 else ''}")

        print("\n💹 Курсы валют:")
        for currency in result['currency_rates']:
            print(f"   • {currency['currency']}: {currency['rate']} руб")

        print("\n📊 Акции S&P500:")
        for stock in result['stock_prices']:
            print(f"   • {stock['stock']}: ${stock['price']}")

        print("\n" + "=" * 60)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Проект готов к дальнейшей разработке! 🚀")

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        print(f"❌ Ошибка: Файл не найден! Проверь путь: {file_path}")
        print("💡 Убедись, что файл operations.xlsx находится в папке data/")

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        print(f"❌ Критическая ошибка: {e}")
        print("🔧 Проверь логи в файле 'bank_analysis.log'")


if __name__ == "__main__":
    main()