import json
import hashlib
from typing import List


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, control_sum: str) -> None:
    """
    Выгружает контрольную сумму по csv-файлу
    
    :param variant: номер варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    pass
    
    result = {
        "variant": variant,
        "checksum": control_sum
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
