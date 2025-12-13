import re
from typing import List, Dict
from checksum import serialize_result, calculate_checksum
from read_file import read_csv

VARIANT = 61
PATTERN = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "http_status_message": r"^[1-5][0-9]{2} [A-Za-z ]+$",
    "inn": r"^\d{12}$",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "ip_v4": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
    "latitude": r"^-?(?:90(?:\.0+)?|[1-8]?[0-9](?:\.[0-9]+)?)$",
    "hex_color": r"^#[0-9a-fA-F]{6}$",
    "isbn": r"^(?:\d{1,5}-)?\d{1,7}-\d{1,7}-\d{1,7}-[\dX]$",
    "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    "time": r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{1,6})?$",
}

def validate_row(row: dict, pattern: dict[str, str]) -> bool:
    """
    Проверяет инвалидность строки по паттерну

    :param row: строки csv файла для итерации
    :param patterns: паттерн словаря
    :return True/False: csv файл не имеет / имеет все инвалидные строки

    """
    for field, pattern in pattern.items():
        value = row.get(field, '').strip()
        if not re.fullmatch(pattern, value):
            return False
    return True

def check_invalid_rows(rows: List[dict], pattern: Dict[str, str]) -> List[int]:
    """
    Обнаруживает строки, неподходящие под паттерн

    :param rows: строки файла
    :param pattern: паттерн файла данных
    :return: возвращает некорректные строки 
    """
    invalid_rows = []
    for i, row in enumerate(rows):
        if not validate_row(row, pattern):
            invalid_rows.append(i)
    return invalid_rows

def main() -> None:
    """
    Считывает данные с csv файла. Подсчитывает количество некорректных строк.
    Записывает результат в json
    """
    rows = read_csv('61.csv')

    invalid_rows = check_invalid_rows(rows, PATTERN)
    control_sum = calculate_checksum(invalid_rows)

    serialize_result(VARIANT, control_sum)
    print(f"Контрольная сумма: {control_sum}")

if __name__ == "__main__":
    main()
