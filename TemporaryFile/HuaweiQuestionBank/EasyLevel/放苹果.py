def f(m,n):
    if m<0 or n<0:
        return 0
    elif m==1 or n==1:
        return 1
    else:
        return f(m,n-1)+f(m-n,n)
while True:
    try:
        m,n=map(int,input().split())
        print(f(m,n))
    except:
        break