import statistics

import random


def kth(array: list, k: int) -> int:
    if len(array) == 1:
        return array[0]

    pivot_idx = random.randint(0, len(array) - 1)
    pivot = array[pivot_idx]

    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    if k <= len(left):
        return kth(left, k)
    elif k <= len(left) + len(middle):
        return middle[0]
    else:
        return kth(right, k - len(left) - len(middle))

def find_optimal_position(skewers):
    ys = [skewer[1] for skewer in skewers]

    n = len(ys)

    if n % 2 == 1:
        median_y = kth(ys, n // 2)
    else:
        median_y = (kth(ys, n // 2 - 1), kth(ys, n // 2)) / 2

    return median_y


skewers = [(0, 24), (5, 15), (10, 16)]
optimal_y = find_optimal_position(skewers)
print(f"Оптимальная позиция магистрали: {optimal_y}")