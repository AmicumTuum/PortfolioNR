import csv

filename = 'one.csv'
total = 0

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        total += int(row[3])

print(f'Общая сумма {3} столбца: {total}')