import logging
import os

import pandas as pd
from datetime import datetime


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Настройка логирования для приложения."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("bank-analysis.log"), logging.StreamHandler()],
    )


setup_logging()


def check_file_exists(file_path: str) -> bool:
    """
    Проверяет существование файла.

    Args:
        file_path: Путь к файлу

    Returns:
        True если файл существует, иначе False
    """
    exists = os.path.exists(file_path)
    if not exists:
        logger.warning(f"Файл не найден: {file_path}")
    return exists


def validate_file_extension(file_path: str) -> str:
    """
    Проверяет и возвращает расширение файла.

    Args:
        file_path: Путь к файлу

    Returns:
        Расширение файла (.xlsx, .xls)

    Raises:
        ValueError: Если неподдерживаемый формат
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext not in [".xlsx", ".xls"]:
        error_msg = f"Неподдерживаемый формат файла: {file_ext}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Поддерживаемый формат: {file_ext}")
    return file_ext  # передается как аргумент в функцию get_excel_engine ниже


def get_excel_engine(file_ext: str) -> str:
    """
    Возвращает движок для чтения Excel файла.

    Args:
        file_ext: Расширение файла

    Returns:
        Имя движка ('openpyxl' или 'xlrd')
    """
    engines = {".xlsx": "openpyxl", ".xls": "xlrd"}

    engine = engines.get(file_ext)
    logger.info(f"Выбран движок: {engine} для {file_ext}")
    return engine


def read_excel_file(file_path: str, engine: str) -> pd.DataFrame:
    """
    Читает Excel файл с указанным движком.

    Args:
        file_path: Путь к файлу
        engine: Движок для чтения

    Returns:
        DataFrame с данными
    """
    try:
        logger.info(f"Чтение Excel файла с движком {engine}")
        df = pd.read_excel(file_path, engine = engine)
        logger.info(f"Успешно прочитано строк: {len(df)}")
        return df

    except Exception as e:
        error_msg = f"Ошибка чтения Excel: {e}"
        logger.error(error_msg)
        raise

###################################################################
def get_latest_transaction_date(df: pd.DataFrame) -> str:
    """
    Находит дату последней транзакции в данных.

    Args:
        df: DataFrame с транзакциями

    Returns:
        Строка с датой в формате 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        # Убедимся что даты в правильном формате
        df_temp = df.copy()
        df_temp['Дата операции'] = pd.to_datetime(df_temp['Дата операции'])

        # Находим самую позднюю дату
        latest_date = df_temp['Дата операции'].max()

        # Форматируем в нужный вид
        return latest_date.strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        logger.error(f"Ошибка определения даты последней транзакции: {e}")
        # Возвращаем текущую дату как fallback
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_recent_transactions(df: pd.DataFrame, days: int = 7, limit: int = 10) -> list:
    """
    Находит последние транзакции за указанный период.

    Args:
        df: DataFrame с транзакциями
        days: За сколько дней ищем (по умолчанию 7)
        limit: Сколько транзакций вернуть

    Returns:
        Список последних транзакций
    """
    try:
        df_temp = df.copy()
        df_temp['Дата операции'] = pd.to_datetime(df_temp['Дата операции'])

        # Вычисляем дату начала периода
        end_date = df_temp['Дата операции'].max()
        start_date = end_date - pd.Timedelta(days=days)

        # Фильтруем по периоду
        mask = (df_temp['Дата операции'] >= start_date) & (df_temp['Дата операции'] <= end_date)
        recent_df = df_temp[mask]

        # Сортируем от новых к старым
        recent_df = recent_df.sort_values('Дата операции', ascending=False)

        # Берем нужное количество
        result = []
        for _, row in recent_df.head(limit).iterrows():
            result.append({
                "date": row['Дата операции'].strftime("%d.%m.%Y %H:%M"),
                "amount": round(row['Сумма операции'], 2),
                "category": row.get('Категория', 'Неизвестно'),
                "description": row.get('Описание', 'Без описания'),
                "card": str(row.get('Номер карты', ''))[-4:] if pd.notna(row.get('Номер карты')) else 'N/A'
            })

        logger.info(f"Найдено {len(result)} транзакций за последние {days} дней")
        return result

    except Exception as e:
        logger.error(f"Ошибка поиска последних транзакций: {e}")
        return []