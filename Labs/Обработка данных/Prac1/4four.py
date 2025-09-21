import random

def intersection(list1, list2):
    return [value for value in list1 if value in list2]

list1 = [random.randint(0, 20) for i in range(10)]
list2 = [random.randint(0, 20) for i in range(10)]

print(list1, list2)

print(intersection(list1, list2))