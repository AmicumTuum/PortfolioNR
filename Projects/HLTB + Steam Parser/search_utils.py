import re
import unicodedata

def normalize_title(title: str) -> str:
    """Унифицирует название игры: lowercase, удаление символов, нормализация пробелов и кавычек"""

    # Удаляем кавычки и восклицательные знаки, тире и т.п. напрямую
    replacements = {
        '’': '', '‘': '', '“': '', '”': '', '!': '',
        '–': '', '—': '',
    }
    for k, v in replacements.items():
        title = title.replace(k, v)

    # Удаляем все символы категории Symbol (включая ™, ®, © и др.)
    title = ''.join(ch for ch in title if not unicodedata.category(ch).startswith('S'))

    # Удаляем скобки (круглые)
    title = re.sub(r"[()]", "", title)

    # Удаляем все символы кроме букв, цифр, пробелов, дефисов, запятых и апострофов
    title = re.sub(r"[^\w\d\s:,'\-]", "", title)

    # Заменяем дефисы и двоеточия на пробелы
    title = re.sub(r"[-:]", " ", title)

    # Убираем множественные пробелы
    title = re.sub(r"\s+", " ", title)

    title = unicodedata.normalize('NFKD', title)
    title = title.lower().strip()

    return title.strip()
