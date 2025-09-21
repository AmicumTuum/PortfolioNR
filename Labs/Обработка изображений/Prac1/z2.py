a = int(input("Число a до 30000: "))
b = int(input("Число b до 30000: "))
d = int(input("Число d: "))

rez = 1

for i in range(a-d, b-d+1):
  rez = rez * i
print(rez)