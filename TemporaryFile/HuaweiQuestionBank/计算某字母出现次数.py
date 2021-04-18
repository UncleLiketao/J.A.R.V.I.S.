def get_count():
    fir_line = input().lower()
    sec_line = input().lower()
    count = fir_line.count(sec_line)
    return count
print(get_count())