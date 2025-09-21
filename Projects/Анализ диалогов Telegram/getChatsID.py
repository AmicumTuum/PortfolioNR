import csv
from telethon.sync import TelegramClient

api_id = ''
api_hash = ''
phone_number = ''

client = TelegramClient('session_name', api_id, api_hash, system_version="4.16.30-vxCUSTOM")

async def get_chat_id():
    async with client:
        dialogs = await client.get_dialogs()
        # Открываем файл для записи
        with open('IDs.csv', 'w', encoding='utf-8', newline='') as csvfile:
            # Создаем объект writer
            writer = csv.writer(csvfile, delimiter=';')
            # Записываем заголовки
            writer.writerow(['Chat Title', 'Chat ID'])
            # Записываем данные из dialogs
            for dialog in dialogs:
                writer.writerow([dialog.title, dialog.id])

client.loop.run_until_complete(get_chat_id())