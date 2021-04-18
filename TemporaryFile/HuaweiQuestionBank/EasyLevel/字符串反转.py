input_string = input()
is_input_string_lower = input_string.islower()
if is_input_string_lower and len(input_string) < 1000:
    print(input_string[::-1])
else:
    print("输入范围错误")