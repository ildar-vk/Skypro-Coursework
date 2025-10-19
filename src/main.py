import json
import pandas as pd
from views import home_page
from utils import check_file_exists, validate_file_extension, get_excel_engine, read_excel_file


def main():
    """
    Главная функция - анализ банковских операций.
    """
    try:
        print("🚀 Запуск анализа банковских операций...")

        # 1. Используем функции для чтения
        file_path = "data/operations.xlsx"

        # Проверяем существование файла
        if not check_file_exists(file_path):
            print("❌ Файл не найден! Завершаем работу.")
            return

        # Получаем движок для чтения
        file_ext = validate_file_extension(file_path)
        engine = get_excel_engine(file_ext)

        # Читаем файл - получаем df
        df = read_excel_file(file_path, engine)
        print(f"✅ Загружено {len(df)} транзакций")

        if df.empty:
            print("❌ Нет данных для анализа!")
            return

        # 2. Генерируем главную страницу (БЕЗ target_date!)
        print("📊 Генерация главной страницы...")
        home_data = home_page(df)  # ← Убрали target_date!

        # 3. Простая статистика
        print("🔍 Базовая статистика...")
        simple_analysis = {
            "total_transactions": len(df),
            "expense_transactions": len(df[df['Сумма операции'] < 0]),
            "income_transactions": len(df[df['Сумма операции'] > 0]),
            "total_spent": round(abs(df[df['Сумма операции'] < 0]['Сумма операции'].sum()), 2),
            "total_income": round(df[df['Сумма операции'] > 0]['Сумма операции'].sum(), 2)
        }

        # 4. Сохраняем результаты
        print("💾 Сохранение результатов...")

        # Главная страница
        with open("output/home_page.json", "w", encoding="utf-8") as f:
            json.dump(home_data, f, indent=2, ensure_ascii=False)

        # Статистика
        with open("output/analysis_stats.json", "w", encoding="utf-8") as f:
            json.dump({
                "status": "success",
                "file_info": {
                    "path": file_path,
                    "extension": file_ext,
                    "engine": engine
                },
                "transactions": simple_analysis,
                "generated_at": pd.Timestamp.now().isoformat()
            }, f, indent=2, ensure_ascii=False)

        # 5. Выводим результаты
        print("\n📈 РЕЗУЛЬТАТЫ АНАЛИЗА:")
        print(f"   📁 Файл: {file_path} ({file_ext})")
        print(f"   🔧 Движок: {engine}")
        print(f"   📊 Всего транзакций: {simple_analysis['total_transactions']}")
        print(f"   💸 Расходы: {simple_analysis['expense_transactions']} операций")
        print(f"   💰 Доходы: {simple_analysis['income_transactions']} операций")
        print(f"   🏦 Общая сумма расходов: {simple_analysis['total_spent']:.2f} руб.")
        print(f"   🏦 Общая сумма доходов: {simple_analysis['total_income']:.2f} руб.")

        if 'cards' in home_data and home_data['cards']:
            print(f"   💳 Проанализировано карт: {len(home_data['cards'])}")
            for card in home_data['cards']:
                print(f"      *{card['last_digits']}: {card['total_spent']:.2f} руб.")

        print("\n🎉 Анализ завершен успешно!")

    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()