while True:
    try:
        n=int(input())
        res=-1
        if n<=2:
            res=-1
        elif n%2==1:
            res=2
        elif n%4==0:
            res=3
        else:
            res=4
        print(res)
    except:
        break