import re
import logging

logger = logging.getLogger(__name__)

def parse_time_to_hours(value):
    """
    Парсит строковое или числовое значение времени прохождения игры в часы.
    Возвращает float (часы) или 0, если не удалось распарсить.
    """
    try:
        if isinstance(value, (int, float)):
            hours = round(float(value), 2)
            logger.debug(f"Прямое числовое значение времени: {hours} ч")
            return hours

        text = str(value).lower().strip()

        if "less than" in text:
            logger.debug(f"Интерпретируем 'less than' как 0.5 часа")
            return 0.5

        if "½" in text:
            text = text.replace("½", ".5")
            logger.debug(f"Заменили '½' на '.5' в строке: {text}")

        match = re.search(r'([\d.]+)\s*hour', text)
        if match:
            hours = round(float(match.group(1)), 2)
            logger.debug(f"Найдено часы: {hours} ч (из '{value}')")
            return hours

        match = re.search(r'([\d.]+)\s*min', text)
        if match:
            hours = round(float(match.group(1)) / 60, 2)
            logger.debug(f"Найдено минуты: {hours} ч (из '{value}')")
            return hours

        logger.warning(f"Не удалось распарсить время: {repr(value)}")
        return 0
    except Exception as e:
        logger.error(f"Ошибка при парсинге времени {repr(value)}: {e}")
        return 0
