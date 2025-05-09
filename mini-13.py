import statistics

import random


def kth(array: list, k: int) -> int:
    if len(array) == 1:
        return array[0]

    #pivot = random.choice(array)

    #left = [x for x in array if x < pivot]
    #middle = [x for x in array if x == pivot]
    #right = [x for x in array if x > pivot]

    def partition_lomuto(arr, low, high):
        pivot_index = random.randint(low, high)
        arr[low], arr[pivot_index] = arr[pivot_index], arr[low]
        pivot = arr[low]

        l, h, c = low, low, low + 1
        while c <= high:
            if arr[c] < pivot:
                arr[c], arr[h + 1] = arr[h + 1], arr[c]
                arr[h + 1], arr[l] = arr[l], arr[h + 1]
                l += 1
                h += 1
                c += 1
            elif arr[c] == pivot:
                arr[h + 1], arr[c] = arr[c], arr[h + 1]
                h += 1
                c += 1
            else:
                c += 1

        return l, h

    l, h = partition_lomuto(array, 0, len(array) - 1)


    if k < l:
        return kth(array[:l], k)
    elif k <= h:
        return array[l]
    else:
        return kth(array[h + 1:], k - h - 1)

def find_optimal_position(skewers):
    ys = [skewer[1] for skewer in skewers]

    n = len(ys)

    if n % 2 == 1:
        median_y = kth(ys, n // 2 + 1)
    else:
        median_y = (kth(ys, n // 2 - 1) + kth(ys, n // 2)) / 2

    return median_y


skewers = [(0, 24), (5, 15), (10, 16), (34, 18)]
optimal_y = find_optimal_position(skewers)
print(f"Оптимальная позиция магистрали: {optimal_y}")