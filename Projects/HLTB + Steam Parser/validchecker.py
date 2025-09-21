import csv
import requests
import re
import time

#input_filename = 'games_with_times.csv'
input_filename = 'validated_novalid.csv'
output_filename = 'validated_games.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

def extract_steam_app_id(page_text):
    match = re.search(r'https://store\.steampowered\.com/app/(\d+)/', page_text)
    return match.group(1) if match else None

with open(input_filename, newline='', encoding='utf-8') as infile, \
     open(output_filename, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Corrected_APP_ID']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    total = sum(1 for _ in open(input_filename, encoding='utf-8')) - 1
    infile.seek(0)
    next(reader)  # skip header again after seek

    for i, row in enumerate(reader, 1):
        hltb_id = row['HLTB_ID']
        declared_app_id = row['APP_ID']
        name = row.get('Name') or row.get('NAME') or '[No Name]'

        print(f"[{i}/{total}] Проверяю {name} (HLTB_ID: {hltb_id}, заявленный APP_ID: {declared_app_id})...")

        url = f'https://howlongtobeat.com/game/{hltb_id}'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            actual_app_id = extract_steam_app_id(response.text)

            if actual_app_id and actual_app_id != declared_app_id:
                print(f"  ⚠️ Айди не совпадает! Найден: {actual_app_id}")
                row['Corrected_APP_ID'] = actual_app_id
            else:
                print(f"  ✅ Совпадает или не найдено. Записываю как есть.")
                row['Corrected_APP_ID'] = ''
        except Exception as e:
            print(f"  ❌ Ошибка при загрузке страницы: {e}")
            row['Corrected_APP_ID'] = 'ERROR'

        writer.writerow(row)
        time.sleep(1.5)
