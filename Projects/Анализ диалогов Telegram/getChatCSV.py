import os
from telethon.sync import TelegramClient
import csv

api_id = ''
api_hash = ''
phone_number = '+'

client = TelegramClient('session_name', api_id, api_hash, system_version="4.16.30-vxCUSTOM")

async def export_chat(chat_id, limit=100):
    output_folder = "chats"
    filename = os.path.join(output_folder, f"{chat_id}_chat.csv")
    messages = await client.get_messages(chat_id, limit=limit)
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['date', 'sender_id', 'sender_username', 'message', 'forwarded_from', 'reply_to_msg_id', 'media']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for message in messages:
            writer.writerow({
                'date': message.date,
                'sender_id': message.sender_id,
                'sender_username': message.sender.username,
                'message': message.text,
                'forwarded_from': message.fwd_from,
                'reply_to_msg_id': message.reply_to_msg_id,
                'media': message.media
            })

with client:
    chat_id = 1010335941
    exported_file = client.loop.run_until_complete(export_chat(chat_id, limit=100000))