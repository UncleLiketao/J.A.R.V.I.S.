def count(n):
    ndic = {}
    for i in range(1, n + 1):
        ndic[i] = 1
    for i in range(2, n):
        for j in range(i + 1, n // i + 1):
            ndic[i * j] = ndic[i * j] + i + j
    sum = 0
    for i in range(2, n):
        if ndic[i] == i:
            sum += 1
    return sum


while True:
    try:
        print(count(int(input())))
    except:
        break