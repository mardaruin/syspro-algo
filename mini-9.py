import random
import string

def lsd_radix_sort(strings):
    max_length = len(max(strings, key=len))

    for i in range(max_length - 1, -1, -1):
        buckets = {}
        #buckets = [[] for _ in range(256)]

        for string in strings:
            if i < len(string):
                char_code = ord(string[i])
            else:
                char_code = 0

            if char_code not in buckets:
                buckets[char_code] = []
            buckets[char_code].append(string)

        strings = []
        for char_code in sorted(buckets.keys()):
            strings.extend(buckets[char_code])

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