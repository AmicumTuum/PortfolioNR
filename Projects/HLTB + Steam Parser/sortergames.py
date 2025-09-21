import pandas as pd

# Загрузка исходного файла
df = pd.read_csv('games_with_times.csv')

# Фильтрация:
filtered = df[
    (df['Achievements'] != '0/0') &
    (pd.to_numeric(df['Completionist'], errors='coerce') > 0) &
    (df['Achievements'].str.split('/').str[0] != df['Achievements'].str.split('/').str[1])
].copy()

# Сортировка
filtered['Completionist'] = pd.to_numeric(filtered['Completionist'], errors='coerce')
filtered = filtered.sort_values(by='Completionist', ascending=True)

# Сохранение
filtered.to_csv('games_sorted_by_completionist.csv', index=False)

print("✅ Готово! Сохранено в games_sorted_by_completionist.csv")
