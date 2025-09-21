import time
import asyncio
from datetime import datetime, timedelta
from config import config
from logger_setup import setup_logger
from steam_api import get_steam_games, get_achievements
from hltb_parser import parse_time_to_hours
from hltb_search import smart_search
from search_utils import normalize_title
from file_utils import read_processed_games, read_not_found_games_with_date, save_not_found_games, append_found_game

logger = setup_logger()

FOUND_FILE = config["FOUND_FILE"]
NOT_FOUND_FILE = config["NOT_FOUND_FILE"]
DAYS_TO_RETRY = config["DAYS_TO_RETRY"]
SAVE_INTERVAL = config.get("SAVE_INTERVAL", 0)
SAVE_INTERVAL_TIME = config.get("SAVE_INTERVAL_TIME", 300)  # в секундах, 0 — не используется
MAX_GAMES = config.get("MAX_GAMES", 0)

async def main():
    # Читаем уже обработанные игры (ключи — нормализованные, значения — оригиналы)
    processed_games_raw = read_processed_games(FOUND_FILE)  # {norm_title: original_title}
    processed_games = set(processed_games_raw.keys())

    # Читаем не найденные игры с датой (ключ — нормализованное, значение — (оригинал, достижения, дата))
    not_found_games_raw = read_not_found_games_with_date(NOT_FOUND_FILE)  
    not_found_games = set(not_found_games_raw.keys())

    already_processed = processed_games.union(not_found_games)
    updated_not_found = not_found_games_raw.copy()

    games = await get_steam_games()

    write_header = not processed_games_raw  # если файл пустой — пишем заголовок

    processed_count = 0
    last_save_time = time.time()

    for i, game in enumerate(games):
        if MAX_GAMES > 0 and i >= MAX_GAMES:
            logger.info(f"Достигнут лимит обработки игр: {MAX_GAMES}. Выход.")
            break

        title_raw = game["name"].strip()
        title_norm = normalize_title(title_raw)
        app_id = game["appid"]

        if title_norm in already_processed:
            logger.debug(f"[DEBUG] norm: {title_norm} not in processed: {title_norm not in already_processed}")
            #logger.info(f"[SKIP] {title_raw} — уже обработана или недавно не найдена")
            continue

        if title_norm in not_found_games_raw:
            _, _, last_tried = not_found_games_raw[title_norm]
            if datetime.today().date() - last_tried < timedelta(days=DAYS_TO_RETRY):
                #logger.info(f"[SKIP] {title_raw} — недавно не найдена ({last_tried})")
                continue

        logger.info(f"🔍 Ищу: {title_raw}")

        best_match = await smart_search(title_raw)

        if best_match:
            time_main_story = parse_time_to_hours(best_match.main_story)
            time_main_extra = parse_time_to_hours(best_match.main_extra)
            time_completionist = parse_time_to_hours(best_match.completionist)
            time_all_styles = parse_time_to_hours(best_match.all_styles)
            achievements = await get_achievements(app_id)

            logger.info(f"✅ {title_raw}: {time_main_story}/{time_main_extra}/{time_completionist}/{time_all_styles}, Achievements: {achievements}")

            append_found_game(FOUND_FILE, [
                title_raw,
                time_main_story,
                time_main_extra,
                time_completionist,
                time_all_styles,
                achievements,
                app_id,
                best_match.game_id if hasattr(best_match, "game_id") else ""
            ], write_header=write_header)

            write_header = False
            updated_not_found.pop(title_norm, None)
        else:
            achievements = await get_achievements(app_id)
            if not achievements:
                achievements = "0/0"
            updated_not_found[title_norm] = (title_raw, achievements, str(app_id), datetime.today().date())
            logger.warning(f"❌ Не найдено в HLTB, записано в not_found: {title_raw} с достижениями {achievements}")

        processed_count += 1

        if SAVE_INTERVAL > 0 and processed_count % SAVE_INTERVAL == 0:
            #logger.info(f"Сохраняем прогресс после {processed_count} игр...")
            save_not_found_games(NOT_FOUND_FILE, updated_not_found)

        if SAVE_INTERVAL_TIME > 0 and (time.time() - last_save_time) >= SAVE_INTERVAL_TIME:
            #logger.info(f"Сохраняем прогресс через {SAVE_INTERVAL_TIME} секунд...")
            save_not_found_games(NOT_FOUND_FILE, updated_not_found)
            last_save_time = time.time()

        await asyncio.sleep(1.5)

    save_not_found_games(NOT_FOUND_FILE, updated_not_found)

if __name__ == "__main__":
    asyncio.run(main())