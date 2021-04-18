def fun(a):
    sum = 0
    while a >= 3:
        sum += a // 3
        a = a //3 + a % 3
    return sum + 1 if a ==2 else sum

while True:
    n = int(input())
    if n ==0:
        break
    print(fun(n))