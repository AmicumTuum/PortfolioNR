import csv
import asyncio
import nltk
from telethon.sync import TelegramClient
from config import API_ID, API_HASH
from sentiment import process_comments, generate_summary
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
from wordcloud import WordCloud
from nltk.corpus import stopwords

api_id = API_ID
api_hash = API_HASH
chat = 'https://t.me/moscowach'
output_file = 'messages_and_replies.csv'

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

async def find_message_by_keywords(client, keywords):
    print("Поиск сообщения по введённому тексту...")
    async for message in client.iter_messages(chat):
        if message.text and any(keyword in message.text for keyword in keywords):
            print(f"Найдено сообщение: {message.text} (ID: {message.id})")
            return message.id
    print("Сообщение с указанным текстом не найдено.")
    return None

async def fetch_replies_for_message(client, message_id):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Sender ID', 'Reply Text', 'Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        async for reply in client.iter_messages(chat, reply_to=message_id):
            if reply.text:
                writer.writerow({
                    'Sender ID': reply.sender_id,
                    'Reply Text': reply.text,
                    'Date': reply.date.strftime('%Y-%m-%d %H:%M:%S')
                })

def plot_results():
    with open('analyzed_comments.csv', 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        if 'Date' not in reader.fieldnames or 'Sentiment' not in reader.fieldnames:
            print("Столбцы 'Date' или 'Sentiment' отсутствуют в файле.")
            return
        
        timestamps = {'Положительный': [], 'Негативный': [], 'Нейтральный': []}
        all_words = []

        for row in reader:
            sentiment = row['Sentiment']
            if sentiment in timestamps:
                try:
                    timestamps[sentiment].append(datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S'))
                except ValueError:
                    print(f"Некорректный формат даты: {row['Date']}")
            all_words.extend(row['Reply Text'].split())

        time_counts = defaultdict(lambda: {'Положительный': 0, 'Негативный': 0, 'Нейтральный': 0})
        for sentiment, dates in timestamps.items():
            for dt in dates:
                key = (dt.month, dt.day, dt.hour)
                time_counts[key][sentiment] += 1

        sorted_times = sorted(time_counts.keys())

        plt.figure(figsize=(12, 6))
        for sentiment in ['Положительный', 'Негативный', 'Нейтральный']:
            counts = [time_counts[time][sentiment] for time in sorted_times]
            time_labels = [f"{month:02d}-{day:02d}-{hour:02d}" for month, day, hour in sorted_times]
            plt.plot(time_labels, counts, marker='o', label=sentiment)

        plt.title('Динамика комментариев по месяц-день-час с разбивкой по настроению')
        plt.xlabel('Месяц-День-Час')
        plt.ylabel('Количество комментариев')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

        # Облако слов
        filtered_words = [word for word in all_words if word.lower() not in stop_words]

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Облако слов из комментариев')
        plt.show()

async def main():
    keywords = input("Введите текст: ").split(',')
    async with TelegramClient('Analyse', api_id, api_hash) as client:
        message_id = await find_message_by_keywords(client, keywords)
        if message_id:
            await fetch_replies_for_message(client, message_id)
            process_comments()
            generate_summary()
            plot_results()

if __name__ == "__main__":
    asyncio.run(main())