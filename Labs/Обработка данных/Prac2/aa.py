from datetime import datetime

a = 9000000000
b = 1053304773
c=3774033501
print (b)
timestamp = c
dt_object = datetime.utcfromtimestamp(timestamp)

print("UTC/GMT time:", dt_object)