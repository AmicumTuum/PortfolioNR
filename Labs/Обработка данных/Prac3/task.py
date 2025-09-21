import pandas as pd
import csv
import numpy as np


listNames = ['длина наружной доли околоцветника', 'ширины наружной доли околоцветника', 'длина внутренней доли околоцветника', 'ширина внутренней доли околоцветника']

csv_reader = pd.read_csv('iris.csv', delimiter=',')
# index_col='variety',  usecols=['sepalLength','sepalWidth','petalLength','petalWidth'], dtype={'sepalLength': np.float32, 'sepalWidth': np.float32, 'petalLength': np.float32, 'petalWidth': np.float32})

sepalLength = csv_reader['sepalLength']
sum_sepalLength = sum(sepalLength)
num_sepalLength = len(sepalLength)
avg_sepalLength = sum_sepalLength/num_sepalLength

print("Средняя", listNames[0], avg_sepalLength, "\n")


sepalWidth = csv_reader['sepalWidth']
num_sepalWidth = len(sepalWidth)
sorted_sepalwidth = sorted(sepalWidth)
middle_sepalwidth = int(num_sepalWidth / 2)

print('Медиана', listNames[1], sorted_sepalwidth[middle_sepalwidth], "\n")
print('Среднее значение', listNames[1], sum(sepalWidth)/len(sepalWidth), "\n")


min_sepalLength = min(sepalLength)
max_sepalLength = max(sepalLength)

print('Выбросы', listNames[0], min_sepalLength, max_sepalLength, "\n")


sepalWidth_counts={}
for i in sepalWidth:
    if i in sepalWidth_counts:
        sepalWidth_counts[i] += 1
    else:
        sepalWidth_counts[i] = 1

max_sepalWidth = 0
mode_sepalWidth = None
for k, v in sepalWidth_counts.items():
    if max_sepalWidth < v:
        max_sepalWidth = v
        mode_sepalWidth = k

print('Мода', listNames[1], mode_sepalWidth, max_sepalWidth, "\n")


min_sepalLength = min(sepalLength)
max_sepalLength = max(sepalLength)
sepalLength_range = max_sepalLength - min_sepalLength
print('Размах', listNames[0], sepalLength_range, "\n")

def stdev(nums):
    diffs = 0
    avg = sum(nums)/len(nums)
    for n in nums:
        diffs += (n - avg)**(2)
    return (diffs/(len(nums)-1))**(0.5)

print('Стандартное отклонение для', listNames[0], stdev(sepalLength), "\n")  # 3.2223917589832167

print('Стандартное отклонение для', listNames[1], stdev(sepalWidth), "\n")  # 36.32240385925089


def dispersia(nums):
    diffs = 0
    avg = sum(nums)/len(nums)
    for n in nums:
        diffs += (n - avg)**(2)
    return ((diffs/(len(nums)-1))**(0.5)*(diffs/(len(nums)-1))**(0.5))

print('Дисперсия для', listNames[0], dispersia(sepalLength), "\n")

print('Дисперсия для', listNames[1], dispersia(sepalWidth), "\n") 