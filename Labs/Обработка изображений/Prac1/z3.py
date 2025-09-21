a = list(map(int, input("Введите числа: ").split()))
rez = 0

for i in range(len (a)):
  if a[i]%4==0 and a[i]%10==6:
      rez = rez + a[i]
print(rez)