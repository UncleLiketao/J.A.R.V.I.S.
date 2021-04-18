while True:
    try:
        n=int(input())
        a=n**2+1-n#首项a=n^2+1-n
        res=str(a)
        for i in range(1,n):
            a=a+2
            res=res+'+'+str(a)
        print(res)
    except:
        break