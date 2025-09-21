import csv

input_file = 'validated_games.csv'
output_file = 'validated_novalid.csv'

with open(input_file, newline='', encoding='utf-8') as csv_in, \
     open(output_file, 'w', newline='', encoding='utf-8') as csv_out:
    
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out)

    # Сохраняем заголовок
    headers = next(reader)
    writer.writerow(headers)

    for row in reader:
        # Проверка: есть ли 9 колонка и она не пуста
        if len(row) >= 9 and row[8].strip():
            writer.writerow(row)

print("✅ Файл сохранён как:", output_file)