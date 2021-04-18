while True:
    try:
        a = input()
        b = input()
        if len(a) > len(b):
            a,b = b,a
        max_length = 0
        i = 0
        while i + max_length < len(a):
            while i + max_length < len(a) and a[i:i + max_length + 1] in b:
                max_length += 1
            i += 1
        print(max_length)
    except:
        break