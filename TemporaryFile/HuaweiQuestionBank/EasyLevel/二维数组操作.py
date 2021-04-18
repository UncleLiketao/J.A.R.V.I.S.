while True:
    try:
        m, n = map(int, input().split())
        x1, y1, x2, y2 = map(int, input().split())
        i_m, i_n = int(input()), int(input())
        x, y = map(int, input().split())
        # 1，数据表行列范围都是[0,9]，若满足输出'0'，否则输出'-1'
        print('0' if (0 <= m <= 9) and (0 <= n <= 9) else '-1')
        # 2，交换的坐标行列数要在输入的表格大小行列数范围[0, m)x[0, n)内
        print('0' if (0 <= x1 < m) and (0 <= y1 < n) and (0 <= x2 < m) and (0 <= y2 < n) else '-1')
        # 3.1，插入的x坐标要在 [0, m) 范围内
        print('0' if (0 <= i_m < m) and (m < 9) else '-1')
        # 3.2，插入的y坐标要在 [0, n) 范围内
        print('0' if (0 <= i_n < n) and (n < 9) else '-1')
        # 4，要检查的位置 (x,y) 要在 [0, m)x[0, n) 内
        print('0' if (0 <= x < m) and (0 <= y < n) else '-1')
    except:
        break