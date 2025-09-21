import os
import csv
from datetime import datetime
import logging
from search_utils import normalize_title

logger = logging.getLogger()

def read_processed_games(filename):
    """
    Возвращаем dict:
    { normalized_title: original_title }
    """
    processed = {}
    if os.path.exists(filename):
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # пропускаем заголовок
                for row in reader:
                    if row:
                        original = row[0].strip()
                        normalized = normalize_title(original)
                        processed[normalized] = original
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {filename}: {e}")
    return processed

def read_not_found_games_with_date(filename):
    """
    Возвращаем dict:
    { normalized_title: (original_title, achievements_str, app_id, last_tried_date) }
    """
    not_found = {}
    if os.path.exists(filename):
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and len(row) >= 4:
                        try:
                            original = row[0].strip()
                            normalized = normalize_title(original)
                            achievements = row[1].strip()
                            app_id = row[2].strip()
                            last_tried = datetime.strptime(row[3], "%Y-%m-%d").date()
                            not_found[normalized] = (original, achievements, app_id, last_tried)
                        except Exception as e:
                            logger.warning(f"Неверный формат данных в {filename}: {e}")
                            not_found[normalized] = (original, "0/0", "", datetime.min.date())
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {filename}: {e}")
    return not_found



def save_not_found_games(filename, data):
    """
    data: dict
    ключ — normalized_title,
    значение — (original_title, achievements, app_id, last_try_date)
    """
    logger.info(f"Попытка сохранить not found игры в файл: {filename}, кол-во записей: {len(data)}")
    try:
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Achievements", "App ID", "Last try"])
            for normalized, (original, achievements, app_id, dt) in sorted(data.items()):
                writer.writerow([original, achievements, app_id, dt.strftime("%Y-%m-%d")])
        logger.info(f"Файл {filename} успешно сохранён")
    except Exception as e:
        logger.error(f"Ошибка при записи файла {filename}: {e}")



def append_found_game(filename, row, write_header=False):
    """
    row: список, где row[0] — оригинальное название игры
    """
    mode = 'a'
    try:
        with open(filename, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Name", "Main Story", "Main + Extra", "Completionist", "All Styles", "Achievements","APP_ID", "HLTB_ID"])
            writer.writerow(row)
    except Exception as e:
        logger.error(f"Ошибка при добавлении записи в {filename}: {e}")
