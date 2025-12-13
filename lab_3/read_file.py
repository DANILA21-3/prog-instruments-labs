import csv

def read_csv(path: str) -> list[dict]:
    """
    Читает CSV файл и возвращает его содержимое в виде списка словарей.
    :param path: путь к CSV файлу для чтения
    :return: список словарей, где каждый словарь представляет строку CSV файла
    """
    with open(path, 'r', encoding='utf-16', newline='') as f:
        data = csv.DictReader(f, delimiter=';')
        return list(data)
    