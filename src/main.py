
from utils import process_bank_file

def main():
    try:
        file_path = "/home/oem/PycharmProjects/Courcework/data/operations.xlsx"
        df = process_bank_file(file_path)
        print(f"Готово! Загружено {len(df)} транзакций")
    except Exception as e:
        print(f"{__name__} Ошибка: {e}")

if __name__ == "__main__":
    main()