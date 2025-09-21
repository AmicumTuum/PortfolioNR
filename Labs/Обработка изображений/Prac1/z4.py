a = list(map(int, input("Введите числа: ").split()))
rez = 1

for i in range(len (a)-1):
  if a[i]%7==0 and a[i]%10==3:
      rez = rez * a[i]
print(rez)