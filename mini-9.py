import random
import string

def lsd_radix_sort(strings):
    if not strings:
        return []

    max_length = len(max(strings, key=len))
    temp = [None] * len(strings)

    for i in range(max_length - 1, -1, -1):
        count = [0] * 257

        for string in strings:
            char_code = ord(string[i]) if i < len(string) else 0
            count[char_code + 1] += 1

        for j in range(256):
            count[j + 1] += count[j]

        for string in strings:
            char_code = ord(string[i]) if i < len(string) else 0
            temp[count[char_code]] = string
            count[char_code] += 1

        strings = temp.copy()

    return strings



strings_to_sort = ["abc", "cba", "bca", "aab"]
sorted_strings = lsd_radix_sort(strings_to_sort)
print(sorted_strings)

def generate_random_strings(length, count):
    result = []
    for _ in range(count):
        result.append(''.join(random.choice(string.ascii_lowercase) for _ in range(length)))
    return result

test_data = generate_random_strings(10, 1000)

expected_result = sorted(test_data)
actual_result = lsd_radix_sort(test_data)

if expected_result == actual_result:
    print("Тест пройден успешно!")
else:
    print("Ошибка! Результаты не совпадают.")