def divmod(current_part, divisor):
    quotient = 0
    remainder = current_part

    while remainder >= divisor:
        remainder -= divisor
        quotient += 1

    return quotient, remainder

def long_division(str_a, str_b):
    a = int(str_a)
    b = int(str_b)

    n = len(str_a)
    m = len(str_b)

    quotient = []
    remainder = 0

    for i in range(n):
        current_part = remainder * 10 + int(str_a[i])

        if current_part >= b:
            next_digit, remainder = divmod(current_part, b)
            quotient.append(next_digit)

        else:
            remainder = current_part
            quotient.append(0)

    while quotient and quotient[0] == 0:
        quotient.pop(0)

    if not quotient:
        quotient = ['0']

    result = ''.join(map(str, quotient))

    return result, remainder

a = '987654321'
b = '5647'
result, remainder = long_division(a, b)
print(result, remainder)

assert(int(b) * int(result) + remainder == int(a))

#алгоритм проходится по каждому символу строки a длины n. на каждом шаге производятся проверка условия и операции сложения, целочисленного деления и взятия остатка
#каждая из операций выполняется за константное время.
#так как длина делимого n, шагов будет ровно n. поэтому общее число операций порядка n*m