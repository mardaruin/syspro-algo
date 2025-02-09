import math

def karatsuba_multiply(x, y) -> int:
    str_x = str(abs(x))
    str_y = str(abs(y))

    max_len = max(len(str_x), len(str_y))

    if max_len < 2:
        return x * y

    str_x = str_x.zfill(max_len)
    str_y = str_y.zfill(max_len)

    half_ind = max_len // 2

    a = str_x[:-half_ind]
    b = str_x[-half_ind:]
    c = str_y[:-half_ind]
    d = str_y[-half_ind:]

    first_step = karatsuba_multiply(int(a), int(c))
    second_step = karatsuba_multiply(int(b), int(d))
    third_step = karatsuba_multiply(int(a) + int(b), int(c) + int(d))
    fourth_step = third_step - second_step - first_step

    result = first_step * (10 ** (2 * half_ind)) + fourth_step * (10 ** half_ind) + second_step

    return result if (x >= 0 and y >= 0) or (x <= 0 and y <= 0) else -result


print(karatsuba_multiply(1234, 5678))
assert(karatsuba_multiply(-1234, 5678) == -1234 * 5678)