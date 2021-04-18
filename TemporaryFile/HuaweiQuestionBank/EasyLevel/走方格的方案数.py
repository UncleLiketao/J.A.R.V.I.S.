#请编写一个函数（允许增加子函数），计算n x m的棋盘格子（n为横向的格子数，m为竖向的格子数）沿着各自边缘线从左上角走到右下角，
#总共有多少种走法，要求不能走回头路，即：只能往右和往下走，不能往左和往上走。 #递归做法
def f(n,m):#从左上角到右下角，每次有两种走法，即右移一布或下移一布；当走到边界，即坐标点其中一个等于0，则只有一种走法
    if n==0 or m==0:
        return 1
    else:
        return f(n-1,m)+f(n,m-1)
while True:
    try:
        n,m=map(int,input().split())
        print(f(n,m))
    except:
        break
