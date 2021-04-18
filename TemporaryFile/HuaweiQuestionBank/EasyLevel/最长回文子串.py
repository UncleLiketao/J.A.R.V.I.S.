while True:
    try:
        s = input()
        m = 0
        for i in range(len(s)):
            if i - m >= 1 and s[i-m-1:i+1] == s[i-m-1:i+1][::-1]:
                m += 2
            elif i - m >= 0 and s[i-m:i+1] == s[i-m:i+1][::-1]:
                m += 1
        if m != 0:
            print(m)
    except:
        break