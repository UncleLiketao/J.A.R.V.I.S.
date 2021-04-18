import sys
class Solution:
    def solve(self, password):
        points = 0
        if len(password) < 4:
            points = 5
        elif 5 <= len(password) <= 7:
            points = 10
        else:
            points = 25

        lower, upper, digit, sign = 0, 0, 0, 0
        for i in range(len(password)-1):
            if password[i].islower():
                lower = 10
            elif password[i].isupper():
                upper = 10
            elif password[i].isdigit():
                if digit < 20:
                    digit += 10
            else:
                if sign == 10:
                    sign = 25
                elif sign == 0:
                    sign = 10

        bonus = 0
        if upper + lower == 10 and digit > 0:
            bonus = 2
        if upper + lower == 10 and digit > 0 and sign > 0:
            bonus = 3
        if upper + lower == 20 and digit > 0 and sign > 0:
            bonus = 5

        points += (lower + upper + digit + sign + bonus)

        if points >= 90:
            return ('VERY_SECURE')
        elif 80 <= points < 90:
            return ('SECURE')
        elif 70 <= points < 80:
            return ('VERY_STRONG')
        elif 60 <= points < 70:
            return ('STRONG')
        elif 50 <= points < 60:
            return ('AVERAGE')
        elif 25 <= points < 50:
            return ('WEAK')
        else:
            return ('VERY_WEAK')

for password in sys.stdin:
    s = Solution()
    print(s.solve(password))