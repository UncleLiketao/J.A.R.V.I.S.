while True:
    try:
        in_str = input()
        if len(in_str) > 5000 or len(in_str) == 0:
            raise Exception

        last = in_str.strip().split(" ")[-1]
        leng = len(last)
        print(leng)
        break
    except Exception:
        print("字符串非空且长度小于5000，请再次输入：")