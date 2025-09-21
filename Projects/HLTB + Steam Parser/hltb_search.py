import logging
import asyncio
from howlongtobeatpy import HowLongToBeat
from rapidfuzz import fuzz
from aliases import CUSTOM_IDS
from search_utils import normalize_title

logger = logging.getLogger(__name__)

async def search_hltb(original_title: str):
    hltb = HowLongToBeat()
    try:
        normalized_query = normalize_title(original_title)

        # Пробуем сначала нормализованное название
        results = await asyncio.to_thread(hltb.search, normalized_query)

        # Если не найдено — пробуем оригинальное название
        if not results:
            logger.info(f"🔄 Не найдено по нормализованному названию: '{normalized_query}', пробуем оригинальное: '{original_title}'")
            results = await asyncio.to_thread(hltb.search, original_title)

        if not results:
            logger.info(f"❌ Не найдено ничего по названию: '{original_title}'")
            return None

        for result in results:
            if normalize_title(result.game_name) == normalized_query:
                logger.info(f"✅ Точное совпадение: '{result.game_name}'")
                return result

        best_match = max(results, key=lambda r: fuzz.ratio(normalize_title(r.game_name), normalized_query))
        best_score = fuzz.ratio(normalize_title(best_match.game_name), normalized_query)

        logger.debug(f"🤔 Fuzzy match для '{original_title}': '{best_match.game_name}' с похожестью {best_score}")

        if best_score >= 85:
            return best_match

        return None

    except Exception as e:
        logger.error(f"Ошибка при поиске на HowLongToBeat: {e}")
        return None

async def smart_search(original_title: str):
    # Этап 0 — Поиск по ID, если есть в словаре
    if original_title in CUSTOM_IDS:
        try:
            result = await HowLongToBeat().async_search_from_id(CUSTOM_IDS[original_title])
            if result:
                logger.info(f"🎯 Найдено по ID для '{original_title}'")
                return result
        except Exception as e:
            logger.error(f"Ошибка при поиске по ID для '{original_title}': {e}")

    # Этап 1 — Прямой текстовый поиск с точным и fuzzy совпадением
    result = await search_hltb(original_title)
    if result:
        logger.info(f"🎯 Найдено '{original_title}' через обычный поиск")
        return result

    logger.warning(f"❌ Не найдено: {original_title}")
    return None
