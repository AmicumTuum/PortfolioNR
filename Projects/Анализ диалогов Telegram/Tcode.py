import matplotlib.pyplot as plt
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

from datetime import timedelta
from datetime import datetime

filename = f"chats/X_chat.csv"
IDs = "IDs.csv"

# Получаем текущую дату и время
current_date = datetime.now().strftime("%d.%m.%Y %H:%M")

# Извлечение даты последнего сообщения

import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Preprocess text: remove stopwords
def preprocess_text(text):
    stop_words = set(stopwords.words('russian'))
    word_tokens = word_tokenize(text)
    filtered_text = [word.lower() for word in word_tokens if word.isalpha() and word.lower() not in stop_words]
    return filtered_text

# Загрузка данных из файла (замените путь к файлу на свой)
df = pd.read_csv(filename, keep_default_na=False)
df2 = pd.read_csv(IDs, encoding='utf8', delimiter=";")

match = re.search(r'-?\d+', filename)
if match:
    numbers = int(match.group())
chat_ids = df2['Chat ID'].tolist()

# Проходим по каждой строке df2
for index, row in df2.iterrows():
    # Сравниваем значение из df2 с нашим значением
    if row['Chat ID'] == numbers:
        # Если найдено совпадение, выводим первый столбец и завершаем цикл
        chat_name_matched = row.iloc[0]
        break

# Словарь со значениями для замены
replace_dict = {'Kalextg': 'Л.', 'KVAkushkalera': 'Лера', 'novack59': 'Денис', 'OwakonMex': 'Owakon', 'Volsoren': 'Егор', 'IYRIDOROGAIKIN': 'Юра'}

df['sender_username'] = df['sender_username'].replace(replace_dict)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])
df['date'] += timedelta(hours=4)

last_message_date_str = df['date'].iloc[0]   # Предполагается, что столбец с датой называется 'date'
last_message_date_custom_timezone = pd.to_datetime(last_message_date_str).strftime("%d.%m.%Y %H:%M")

# Additional column for day-only dates
df['day'] = df['date'].dt.date

# Создание нового столбца time_of_day
df['time_of_day'] = pd.cut(df['date'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Ночь (0-6)', 'Утро (6-12)', 'День (12-18)', 'Вечер (18-24)'])

# Создаем столбец с датой (без времени)
df['date_only'] = df['date'].dt.date

# Подсчитываем количество слов для каждой даты
words_per_day = df.groupby('date_only')['message'].apply(lambda x: x.str.split().str.len().sum())

# Рассчитываем среднее количество слов в день
average_words_per_day = words_per_day.mean()

# Подсчитываем количество сообщений для каждой даты
messages_per_day = df['date_only'].value_counts()

# Рассчитываем среднее количество сообщений в день
average_messages_per_day = messages_per_day.mean()

# Подсчет сообщений по времени суток
messages_by_time_of_day = df['time_of_day'].value_counts()
messages_by_time_of_day.columns = ['Время суток', 'Количество сообщений']
time_of_day_order = ['Ночь (0-6)', 'Утро (6-12)', 'День (12-18)', 'Вечер (18-24)']
# Создаем объект Series с указанным порядком сортировки
messages_by_time_of_day = messages_by_time_of_day.reindex(time_of_day_order)

# Count messages per day
messages_per_day = df['day'].value_counts().head(10)

# Total number of messages in the dialog
total_messages_in_dialog = len(df)

# Count messages and percentage per day of the week
day_of_week_stats = df['date'].dt.day_name().value_counts()
total_messages = day_of_week_stats.sum()
percentage_per_day_of_week = (day_of_week_stats / total_messages) * 100

# Статистика: количество сообщений от каждого пользователя
user_message_count = df['sender_username'].value_counts()
total_messages = user_message_count.sum()

# Процентное соотношение
user_message_percentage = (user_message_count / total_messages) * 100
user_message_percentage_red = user_message_percentage.round(2).sort_values(ascending=False)

# Сортировка пользователей по количеству сообщений
sorted_users = user_message_count.sort_values(ascending=False)

# Анализ частоты появления слов
all_messages = ' '.join(df['message'].astype(str))
filtered_text = preprocess_text(all_messages)

word_frequency = pd.Series(filtered_text).value_counts()

# Инициализация счетчиков
forwarded_messages_count = 0
replies_count = 0
links_count = 0
photos_count = 0
videos_count = 0
words_count = 0
stickers_count = 0
voices_count = 0

def count_words(message):
    global words_count
    # Токенизация текста сообщения и подсчет слов
    words = word_tokenize(str(message))
    words_count += len(words)
    return len(words)

# Добавление столбца с количеством слов в каждом сообщении
df['word_count'] = df['message'].apply(count_words)

# Группировка данных по пользователям и подсчет общего количества слов
user_word_counts = df.groupby('sender_username')['word_count'].sum()

# Процентное соотношение
user_words_percentage = (user_word_counts / words_count) * 100
user_words_percentage_red = user_words_percentage.round(2).sort_values(ascending=False)

# Функция для подсчета ссылок в тексте сообщения
def count_links(message):
    global links_count
    # Регулярное выражение для поиска URL
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    # Поиск ссылок в тексте сообщения
    links = re.findall(url_pattern, message)
    # Увеличение счетчика
    links_count += len(links)

# Итерация по каждому сообщению в DataFrame
for index, row in df.iterrows():
    # Подсчет пересланных сообщений
    if pd.notna(row['forwarded_from']) and row['forwarded_from'] != '':
        forwarded_messages_count += 1

    # Подсчет ответов на сообщения
    if pd.notna(row['reply_to_msg_id']) and row['reply_to_msg_id'] != '':
        replies_count += 1
    
    # Подсчет фото
    if pd.notna(row['media']) and 'photo' in row['media']:
        photos_count += 1

    if pd.notna(row['media']) and 'document' in row['media']:
        stickers_count += 1
    
    # Подсчет видео
    if pd.notna(row['media']) and 'DocumentAttributeVideo' in row['media']:
        videos_count += 1

    # Подсчет голосовых
    if pd.notna(row['media']) and "mime_type='audio/ogg'" and 'DocumentAttributeAudio' in row['media']:
        voices_count += 1    

    # Подсчет слов в сообщении
    count_words(row['message'])

    count_links(row['message'])

# Путь к папке
folder_path = f'analysed/{chat_name_matched}/'

# Проверяем существует ли папка
if not os.path.exists(folder_path):
    # Создаем папку, если она не существует
    os.makedirs(folder_path)

output_folder = f"analysed/{chat_name_matched}"
output_file_path = os.path.join(output_folder, f'{chat_name_matched}.txt')

with open(output_file_path, 'w', encoding='utf-8') as file:
    # Записываем текущую дату в файл
    file.write("Дата анализа: " + current_date + "\n")

    file.write("Дата импорта чата: " + last_message_date_custom_timezone+ "\n\n")

    file.write("Общее количество сообщений в диалоге:\n")
    file.write(str(total_messages_in_dialog) + '\n\n')

    file.write("Общее количество голосовых сообщений в диалоге:\n")
    file.write(str(voices_count) + '\n\n')

    file.write("Количество фото:\n")
    file.write(str(photos_count) + '\n\n')

    file.write("Количество видео:\n")
    file.write(str(videos_count) + '\n\n')

    file.write("Количество стикеров:\n")
    file.write(str(stickers_count) + '\n\n')

    file.write("Количество пересланных сообщений:\n")
    file.write(str(forwarded_messages_count) + '\n\n')

    file.write("Количество ответов:\n")
    file.write(str(replies_count) + '\n\n')

    file.write("Количество ссылок:\n")
    file.write(str(links_count) + '\n\n')

    file.write("Количество голосовых:\n")
    file.write(str(voices_count) + '\n\n')

    file.write("Количество слов:\n")
    file.write(str(words_count) + '\n\n')

    file.write("Количество сообщений от каждого пользователя:\n")
    file.write(str(user_message_count.to_string(header=False)) + '\n\n')

    file.write("Процентное соотношение (сообщения):\n")
    file.write(str(user_message_percentage_red.to_string(header=False)) + '\n\n')

    file.write("Количество слов от каждого пользователя:\n")
    file.write(str(user_word_counts.to_string(header=False)) + '\n\n')

    file.write("Процентное соотношение (слова):\n")
    file.write(str(user_words_percentage_red.to_string(header=False)) + '\n\n')

    file.write("Частота появления слов (топ 50):\n")
    file.write(str(word_frequency.head(50).to_string()) + '\n\n')

    file.write("Среднее количество сообщений в день:\n")
    file.write(str(average_messages_per_day) + '\n\n')

    file.write("Среднее количество слов в день:\n")
    file.write(str(average_words_per_day) + '\n\n')

    file.write("Статистика по дням недели:\n")
    russian_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for day, count, percentage in zip(russian_days, day_of_week_stats, percentage_per_day_of_week):
        file.write(f"{day:<15} {count:<5} ({percentage:.2f}%)\n")

    file.write("\nКоличество сообщений по времени суток\n")
    file.write(str(messages_by_time_of_day.to_string(header=False)) + '\n')

    file.write("\nТоп 10 дней по количеству сообщений:\n")
    file.write(str(messages_per_day.to_string(header=False)) + '\n')

# Группировка данных по пользователям и дням, подсчет сообщений
user_messages_per_day = df.groupby(['sender_username', 'day']).size().reset_index(name='count')

# Создание списка всех дней в диапазоне
all_days = pd.date_range(df['day'].min(), df['day'].max())

# Создание пустого DataFrame с индексом по всем дням и столбцами для каждого пользователя
empty_df = pd.DataFrame(index=all_days)

# Заполнение пустого DataFrame данными о количестве сообщений для каждого пользователя
for user, data in user_messages_per_day.groupby('sender_username'):
    user_data = data.set_index('day')['count']
    user_data = user_data.reindex(all_days, fill_value=0)
    empty_df[user] = user_data.values

# Создание графика с большим размером
plt.figure(figsize=(10, 6))  # Установка размера фигуры

for user in empty_df.columns:
    line, = plt.plot(empty_df.index, empty_df[user], label=user, marker='o', markersize=4, linestyle='-')  # linestyle='-': соединить точки
    
    # Получение цвета линии и установка его тексту
    color = line.get_color()
    
    # Добавление точного значения над каждой точкой, если значение не равно нулю
    for x, y in zip(empty_df.index, empty_df[user]):
        if y != 0:
            plt.text(x, y, f'{y}', ha='center', va='bottom', color=color, bbox=dict(facecolor='white', alpha=0.5))  # Устанавливаем цвет текста

# Добавление сетки
plt.grid(True)

# Настройка графика
plt.title('Количество сообщений пользователей в день')
plt.xlabel('Дата')
plt.ylabel('Количество сообщений')
plt.xticks(rotation=45)
plt.legend()

# Сохраняем график в файл
plt.savefig(f'analysed/{chat_name_matched}/{chat_name_matched}_messages.png', dpi=1200, bbox_inches='tight')
plt.show()

user_words_per_day = df.groupby(['sender_username', 'day'])['message'].apply(lambda x: x.str.split().str.len().sum()).reset_index(name='word_count')

# Создание списка всех дней в диапазоне, включая следующий день после последнего дня
all_days = pd.date_range(df['day'].min(), df['day'].max())

# Создание пустого DataFrame с индексом по всем дням и столбцами для каждого пользователя
empty_df = pd.DataFrame(index=all_days)

# Заполнение пустого DataFrame данными о количестве слов для каждого пользователя
for user, data in user_words_per_day.groupby('sender_username'):
    user_data = data.set_index('day')['word_count']
    user_data = user_data.reindex(all_days, fill_value=0)
    empty_df[user] = user_data.values

# Создание графика с большим размером
plt.figure(figsize=(10, 6))  # Установка размера фигуры

for user in empty_df.columns:
    line, = plt.plot(empty_df.index, empty_df[user], label=user, marker='o', markersize=4, linestyle='-')  # linestyle='-': соединить точки
    
    # Получение цвета линии и установка его тексту
    color = line.get_color()

    # Добавление точного значения над каждой точкой, если значение не равно нулю
    for x, y in zip(empty_df.index, empty_df[user]):
        if y != 0:
            plt.text(x, y, f'{y}', ha='center', va='bottom', color=color, bbox=dict(facecolor='white', alpha=0.5))    # ha='center', va='bottom': выравнивание текста

# Добавление сетки
plt.grid(True)

# Настройка графика
plt.title('Количество слов пользователей в день')
plt.xlabel('Дата')
plt.ylabel('Количество сообщений')
plt.xticks(rotation=45)
plt.legend()

# Сохраняем график в файл
plt.savefig(f'analysed/{chat_name_matched}/{chat_name_matched}_words.png', dpi=1200, bbox_inches='tight')
plt.show()