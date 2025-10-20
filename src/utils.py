import logging
import os
import sys
import pandas as pd


def setup_logging() ->None:
    """Настраиваем логирование"""
    logging.basicConfig( level=logging.INFO,
                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         handlers=[logging.FileHandler('bank-analysis.log',mode='w', encoding='utf-8')
                        ,logging.StreamHandler(sys.stdout)],
    )
    print("Логирование настроено. Файл: bank-analysis.log")

setup_logging()


logger = logging.getLogger(__name__)

###Далее идет блок функций для корректной работы с файлом операций###
def check_file(file_path: str) -> bool:
    """Проверяем есть ли файл в директории"""
    exists = os.path.exists(file_path)
    if not exists:
        logger.warning(f'[{__name__}.check_file] Файл не найден в директории: {file_path}')
    return exists


def validate_fail(file_path: str) -> bool:
    """Проверяем и возвращаем расширение файла"""
    file_extension= os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.xlsx', '.xls']:
        error_message = f'[{__name__}.validate_fail] Формат файла не поддерживается {file_extension}'
        logger.error(error_message)
        raise ValueError(error_message)

    logger.info(f'[{__name__}.validate_fail] Верный формат файла {file_extension}')
    return file_extension # Даллее переменая передается в сл. функцию как аргумент


def get_excel_engine(file_extension:str) -> str:
    """Возвращает движок для чтения файла"""
    engins = {'.xlsx': "openpyxl", '.xls': "xlrd"}

    engine = engins.get(file_extension)
    logger.info(f'Выбран: {engine} для {file_extension}')
    return engine


def read_excel_file(file_path: str,engine: str) -> pd.DataFrame:
    """Читаем содержимое файла с указанным движком"""
    try:
        logger.info(f'[{__name__}.read_excel_file] Начало чтения файла {file_path} c движком {engine}')
        df = pd.read_excel(file_path, engine=engine)
        logger.info(f'[{__name__}.read_excel_file] Файл успешно прочитан,\n Количество строк {len(df)}')
        return df
    except Exception as e:
        error_message = f'[{__name__}.read_excel_file] ошибка чтения файла{e}'
        logger.error(error_message)
        raise
## Конец блока кода чтения файлов ###############################################

def process_bank_file(file_path: str) -> pd.DataFrame:
    """
    Главная функция обработки банковского файла.
    Объединяет все этапы: проверка, валидация, чтение.
    """
    logger.info(f"Начало обработки файла: {file_path}")

    # 1. Проверка существования файла
    if not check_file(file_path):
        error_msg = f"СТОП ПРОГРАММЫ! {__name__}/[process_bank_file]->[def check_file]-> {file_path}"
        error_msg_1= f' На функции {__name__}/[process_bank_file] работа программы остановленна! '
        logger.error(error_msg)
        raise ValueError( error_msg_1)

    # 2. Валидация расширения
    file_ext = validate_fail(file_path)

    # 3. Получение движка
    engine = get_excel_engine(file_ext)

    # 4. Чтение файла
    df = read_excel_file(file_path, engine)

    logger.info(f"{__name__}/[process_bank_file] Файл успешно обработан. Загружено {len(df)} транзакций")
    return df
