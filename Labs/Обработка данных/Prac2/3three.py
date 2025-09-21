import numpy as np

arr = np.arange(9).reshape(3, 3)
print("Матрица:    \n", arr)

arr[:, [1, 2]] = arr[:, [2, 1]]
print("Поменяйте местами столбцы 2 и 3:  \n", arr)

arr[:, [0, 2]] = arr[:, [2, 0]]
print("Поменяйте местами столбцы 1 и 3:  \n", arr)

arr[[1, 2], :] = arr[[2, 1], :]
print("Поменяйте местами строки 2 и 3:  \n", arr)

arr[[0, 2], :] = arr[[2, 0], :]
print("Поменяйте местами строки 1 и 3:  \n", arr)