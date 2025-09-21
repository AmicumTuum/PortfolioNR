import httpx
import asyncio
from config import config
import logging

logger = logging.getLogger()

STEAM_API_KEY = config["STEAM_API_KEY"]
STEAM_ID = config["STEAM_ID"]

async def request_with_retry(url, params, max_retries=3, backoff=2, timeout=10):
    """
    Асинхронный GET-запрос с retry и экспоненциальной задержкой.
    """
    delay = backoff
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.get(url, params=params)
                if response.status_code == 400:
                    logger.info(f"Игра {params.get('appid')} не поддерживает достижения (400 Bad Request).")
                    return response
                response.raise_for_status()
                return response
            except httpx.RequestError as e:
                logger.warning(f"Попытка {attempt} не удалась")
                if attempt == max_retries:
                    logger.error(f"Превышено число попыток")
                    raise
                await asyncio.sleep(delay)
                delay *= 2

async def get_steam_games():
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True
    }
    try:
        response = await request_with_retry(url, params)
        games = response.json()['response'].get('games', [])
        return sorted(games, key=lambda g: g['name'].lower())
    except Exception as e:
        logger.error(f"Ошибка при получении игр из Steam: {e}")
        return []

async def get_achievements(app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "appid": app_id
    }
    try:
        response = await request_with_retry(url, params)
        if response.status_code == 400:
            return "0/0"
        data = response.json().get("playerstats", {})
        achievements = data.get("achievements", [])
        if not achievements:
            return "0/0"
        achieved = sum(1 for a in achievements if a.get("achieved", 0) == 1)
        total = len(achievements)
        return f"{achieved}/{total}" if total > 0 else "0/0"
    except Exception as e:
        logger.warning(f"Не удалось получить достижения для app_id {app_id}: {e}")
        return "0/0"
