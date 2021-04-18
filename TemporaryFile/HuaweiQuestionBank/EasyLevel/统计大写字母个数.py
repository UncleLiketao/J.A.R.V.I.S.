while True:
    try:
        n = input()
        c = 0
        for i in n :
            if i.isalpha():
                if i.isupper():
                    c += 1
        print(c)
    except:
        break