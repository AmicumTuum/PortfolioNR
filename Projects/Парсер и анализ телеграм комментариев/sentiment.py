import csv
from transformers import pipeline
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='ru')
sentiment_pipeline = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment")

def analyze_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return 'Нейтральный', 0.0

    result = sentiment_pipeline(text)[0]
    if result['label'] == 'POSITIVE':
        return 'Положительный', result['score']
    elif result['label'] == 'NEGATIVE':
        return 'Негативный', result['score']
    else:
        return 'Нейтральный', result['score']

input_file = 'messages_and_replies.csv'
output_file = 'analyzed_comments.csv'

def process_comments():
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Sender ID', 'Reply Text', 'Sentiment', 'Score', 'Date']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            text = row['Reply Text']
            date = row['Date']
            translated_text = translator.translate(text)
            sentiment, score = analyze_sentiment(translated_text)

            writer.writerow({
                'Sender ID': row['Sender ID'],
                'Reply Text': row['Reply Text'],
                'Sentiment': sentiment,
                'Score': score,
                'Date': date
            })

def generate_summary():
    total = 0
    positive = 0
    negative = 0
    neutral = 0

    with open(output_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            total += 1
            if row['Sentiment'] == 'Положительный':
                positive += 1
            elif row['Sentiment'] == 'Негативный':
                negative += 1
            else:
                neutral += 1

    print("Результаты анализа настроения:")
    print(f"Всего комментариев: {total}")
    print(f"Положительных: {positive} ({positive / total * 100:.2f}%)")
    print(f"Негативных: {negative} ({negative / total * 100:.2f}%)")
    print(f"Нейтральных: {neutral} ({neutral / total * 100:.2f}%)")

    news_sentiment = analyze_news_sentiment(positive, negative, total)
    print(news_sentiment)

def analyze_news_sentiment(positive, negative, total):
    positive_percentage = positive / total * 100
    negative_percentage = negative / total * 100

    if negative_percentage > 40:
        return f"Новость скорее всего негативная. Негативных комментариев: {negative_percentage:.2f}%"
    elif positive_percentage > 40:
        return f"Новость скорее всего положительная. Положительных комментариев: {positive_percentage:.2f}%"
    else:
        return f"Новость нейтральная. Положительных: {positive_percentage:.2f}%, Негативных: {negative_percentage:.2f}%"

if __name__ == "__main__":
    print("Обработка комментариев...")
    process_comments()
    print("Анализ завершен. Генерация отчета...")
    generate_summary()
