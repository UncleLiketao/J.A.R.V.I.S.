while True:
    try:
        year, month, day = map(int, input().split())
        if year <= 0 or month <= 0 or month > 12 or day <= 0 or day > 31:
            print(-1)
        else:
            m = [31, 29, 31, 30, 31, 30, 31, 31,30, 31, 30, 31]
            # 判断是否是闰年
            if (year % 100 == 0 and year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                print(sum(m[:(month-1)])+day)
            else:
                m[1] = 28
                print(sum(m[:(month-1)])+day)
    except EOFError:
        break