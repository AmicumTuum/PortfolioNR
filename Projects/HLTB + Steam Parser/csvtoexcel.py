import pandas as pd

# Загружаем ранее отсортированный CSV
df = pd.read_csv('games_sorted_by_completionist.csv')

# Добавляем колонку "Пройдено"
df['Пройдено'] = ''

# Сохраняем в Excel
df.to_excel('games_list.xlsx', index=False)

print("✅ Файл сохранён как games_list.xlsx")