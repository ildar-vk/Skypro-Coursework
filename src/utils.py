import logging
import os
import sys
from os.path import exists

import pandas as pd
from datetime import datetime

from mypyc.lower.int_ops import lower_int_ge


def setup_logging() ->None:
    """Настраиваем логирование"""
    logging.basicConfig( level=logging.INFO,
                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         handlers=[logging.FileHandler('bank-analisis.log'),logging.StreamHandler(sys.stdout)],
    )


setup_logging()


logger = logging.getLogger(__name__)

###Далее идет блок функций для корректной работы с файлом операций###
def check_file(file_path: str) -> bool:
    """Проверяем есть ли файл в директории"""
    exists = os.path.exists(file_path)
    if not exists:
        logging.warning(f'Файл не найден{file_path}')
    return exists


def validate_fail(file_path: str) -> bool:
    """Проверяем и возвращаем расширение файла"""
    file_extension= os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.xlsx', '.xls']:
        error_message = f'Формат файла не поддерживается {file_extension}'
        logger.error(error_message)
        raise ValueError(error_message)

    logger.info(f'Верный формат файла {file_extension}')
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
        logger.info(f'Начало чтения файла {file_path} c движком {engine}')
        df = pd.read_excel(file_path, engine=engine)
        logger.info(f'Файл успешно прочитан,\n Количество строк {len(df)}')
        return df
    except Exception as e:
        error_message = f'ошибка чтения файла{e}'
        logger.error(error_message)
        raise
## Конец блока кода чтения файлов ###############################################


