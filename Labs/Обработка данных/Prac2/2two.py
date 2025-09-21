import numpy as np

A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
B = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

C = np.reshape(np.concatenate((A, B)), (4, 5))
print("1:","\n", C)


D = np.reshape(np.concatenate((A, B)), (2, 10))
print("2:","\n", D)


def three(A, B):
    return [value for value in A if value in B]

print("3:    ", three(A, B))


def four(A, B):
    return [value for value in A if value not in B]

print("4:    ", four(A, B))

def five(A, B):
    print("5:")
    for i in range(len(A)):
        for j in range(len(B)):
            if A[i] == B[j]:
                print(f"       Число {A[i]} есть в номерах A: {i} и B: {j}")
five(A, B)



def six(A):
    A_temp = []
    for element in A:
        if (element > 3) & (element < 7):
            A_temp.append(element)
    return A_temp

print("6:    ", six(A))

def seven(A, B):
    F = []
    i = 0
    E = [num * 2 for num in B]
    while i < 10:
        F.append(A[i] * E[i])
        i += 1
    return F

print("7:    ",seven(A, B))