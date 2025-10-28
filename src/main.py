import json
import logging

from utils import process_bank_file, setup_logging
from views import home_page


def main() -> None:
    """Главная функция для тестирования ВСЕГО проекта."""
    setup_logging()
    logger = logging.getLogger(__name__)

    print(f"{__name__} Запуск тестирования проекта 'Анализ банковских операций'")
    print("=" * 60)

    try:
        # ТЕСТ 1: Загрузка данных
        file_path = "/home/oem/PycharmProjects/Courcework/data/operations.xlsx"
        print(f"\n ТЕСТ 1: Загрузка данных из Excel {file_path}")
        df = process_bank_file(file_path)
        print(f"Готово! Загружено {len(df)} транзакций")

        # Определяем подходящую дату на основе данных
        if not df.empty and 'Дата операции' in df.columns:
            # Находим максимальную дату в данных
            max_date_str = df['Дата операции'].max()
            try:
                max_date = pd.to_datetime(max_date_str, format='%d.%m.%Y %H:%M:%S')
                # Используем последний день данных как целевую дату
                test_date = max_date.strftime('%Y-%m-%d %H:%M:%S')
                print(f"   • Используем дату из данных: {test_date}")
            except:
                test_date = "2021-12-31 14:30:00"  # fallback
        else:
            test_date = "2021-12-31 14:30:00"  # fallback

        print(f"   • Диапазон дат в данных: от {df['Дата операции'].min()} до {df['Дата операции'].max()}")

        # ТЕСТ 2: Главная страница
        print("\n ТЕСТ 2: Генерация главной страницы...")
        result = home_page(test_date, file_path)

        print("Главная страница сгенерирована успешно!")
        print(f"   • Приветствие: {result['greeting']}")
        print(f"   • Карт проанализировано: {len(result['cards'])}")
        print(f"   • Топ транзакций: {len(result['top_transactions'])}")
        print(f"   • Курсов валют: {len(result['currency_rates'])}")
        print(f"   • Акций: {len(result['stock_prices'])}")

        # Сохраняем полный результат в файл
        with open("home_page_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(" Полный результат сохранен в 'home_page_result.json'")

        # Остальной код остается без изменений...
        # ТЕСТ 3: Показываем пример данных
        print("\n ТЕСТ 3: Пример данных из результата:")

        # Показываем данные по картам
        if result["cards"]:
            print("\n Данные по картам:")
            for card in result["cards"][:3]:  # Показываем первые 3 карты
                last_digits = card.get("last_digits", "0000")
                total_spent = card.get("total_spent", 0)
                cashback = card.get("cashback", 0)
                print(f"     Карта ...{last_digits}:")
                print(f"     Потрачено: {total_spent:,.2f} руб")
                print(f"     Кешбэк: {cashback:,.2f} руб")

        # Показываем топ транзакции
        if result["top_transactions"]:
            print("\n📈 Топ транзакции:")
            for i, transaction in enumerate(result["top_transactions"][:5], 1):
                date = transaction.get("date", "N/A")
                amount = transaction.get("amount", 0)
                category = transaction.get("category", "Не указана")
                description = transaction.get("description", "Без описания")

                # Заменяем 'nan' на 'Не указана'
                if str(category).lower() == "nan":
                    category = "Не указана"

                print(f"   {i}. {date} - {amount:,.2f} руб")
                print(f"      Категория: {category}")
                short_desc = description[:60] + "..." if len(description) > 60 else description
                print(f"      Описание: {short_desc}")

        print("\n Курсы валют:")
        for currency in result["currency_rates"]:
            print(f"   • {currency['currency']}: {currency['rate']} руб")

        print("\n Акции S&P500:")
        for stock in result["stock_prices"]:
            print(f"   • {stock['stock']}: ${stock['price']}")

        print("\n" + "=" * 60)
        print(" ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        print(f"{__name__}->.Теcт 1. Ошибка: Файл не найден! Проверь путь: {file_path}")
        print(" Убедись, что файл operations.xlsx находится в папке data/")

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        import traceback
        logger.error(traceback.format_exc())
        print(f"Критическая ошибка: {e}")
        print("Проверь логи в файле 'bank_analysis.log'")
        traceback.print_exc()

if __name__ == "__main__":
    main()
