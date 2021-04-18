while True:
    try:
        month=int(input())
        n=month-1
        def func(n):
            if n<2:#基线条件
                return 1
            else:#递归条件
                return func(n-1)+func(n-2)
        print(func(n))
    except:
        break
