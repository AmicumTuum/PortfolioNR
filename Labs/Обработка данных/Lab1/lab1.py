import nltk
from nltk.corpus import stopwords
from ebooklib import epub
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd
import re

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

def extract_text_from_epub(file_path):
    book = epub.read_epub(file_path)
    text_content = []

    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.content, 'html.parser')
            text_content.append(soup.get_text())
    
    return '\n'.join(text_content)

def remove_stopwords(text, stop_words):
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

file_path = 'war.epub'
epub_text = extract_text_from_epub(file_path)

text_clean = re.sub(r'[^\w\s]', '', epub_text.lower())

text_no_stopwords = remove_stopwords(text_clean, stop_words)

words = text_no_stopwords.split()

word_counts = Counter(words)

word_freq_df = pd.DataFrame(word_counts.items(), columns=['Слова', 'Частота']).sort_values(by='Частота', ascending=False)

print(word_freq_df.head(25).to_string(index=False))