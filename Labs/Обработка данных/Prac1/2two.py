import random

def unique_list(lst): 
    unique_lst = [] 
    for x in lst: 
        if x not in unique_lst: 
            unique_lst.append(x) 
    return unique_lst 

list = [random.randint(0, 10) for i in range(15)]
print(list)

print(unique_list(list))