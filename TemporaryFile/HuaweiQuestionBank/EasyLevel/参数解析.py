s = input()
flag = 0
start = end = i = sum = 0
res = []
while i < len(s):
    #如果不带引号直接解析
    if s[i] == ' ':
        sum += 1
        end = i
        res.append(s[start:end])
        start = end + 1
     #带引号的需要找到匹配项，依次向前遍历直到找到匹配的引号，最后加入解析
    if s[i] == '"':
        start = i + 1
        flag = 1
        while flag == 1:
            i += 1
            if s[i] == '"':
                end = i
                flag = 0
                res.append(s[start:end])
                end = i = i + 1
                start = end +1#注意这里“”后面有个空格 需要跳过！
    i += 1
if end < len(s):
    res.append(s[start:])
print(len(res))
for i in res:
    print(i)    