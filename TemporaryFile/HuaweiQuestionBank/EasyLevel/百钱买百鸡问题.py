while True:
    try:
        n = int(input())
        # 鸡公最多买20只
        for x in range(21):
            y = (100-7*x)/4 # 鸡母的数量
            z = 100 - x - y # 鸡雏的数量
            if y == int(y) and y >= 0 and z >= 0:
                print(x, int(y), int(z))
    except EOFError:
        break