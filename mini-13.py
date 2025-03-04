import statistics

def find_optimal_position(skewers):
    ys = [skewer[1] for skewer in skewers]

    ys.sort()

    n = len(ys)

    if n % 2 == 1:
        median_y = ys[n // 2]
    else:
        median_y = (ys[(n // 2) - 1] + ys[n // 2]) / 2

    return median_y, statistics.median(ys)


skewers = [(0, 10), (5, 15), (10, 12)]
optimal_y, right_answer = find_optimal_position(skewers)
print(f"Оптимальная позиция магистрали: {optimal_y}, верная позиция: {right_answer}")