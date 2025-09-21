import numpy as np
import random

arr =[random.randint(0,9) for i in range(15)]
print(arr)

def first(arr):
    firstA = []
    for element in arr:
        if element % 2 == 0:
            firstA.append(element)
    return firstA

print('Получившийся массив без нечетных чисел: ', first(arr))

def second(arr):
    secondA = []
    for element in arr:
        if element % 2 == 0:
            secondA.append(element)
        else:
            secondA.append(-1)
    return secondA

print('Получившийся массив с -1: ', second(arr))

def third(arr):
    thirdA = [arr[i:i + 2] for i in range(0, 10, 2)]
    return thirdA

print('Получившийся двумерный массив: ', third(arr))

def fourth(arr):
    fourthA = []
    print(arr)
    for i in range (len(arr)):
        if (i > 5) & (i < 10):
            fourthA.append(arr[i])
    return fourthA

print('Получившийся массив: ', fourth(arr))
