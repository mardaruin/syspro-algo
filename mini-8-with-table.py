import time
import math
import statistics

def run_algorithm(func, args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def classic_matrix_multiply(A, B):
    n = len(A)

    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def split_matrix(A):
    n = len(A)
    mid = n // 2

    a11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    a12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    a21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    a22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]

    assert len(a11) == len(a12) == len(a21) == len(a22), f"Произошла ошибка разделения матриц"
    assert len(a11[0]) == len(a12[0]) == len(a21[0]) == len(a22[0]), f"Произошла ошибка разделения матриц"

    return a11, a12, a21, a22


def add_matrix(A, B):
    if A is None or B is None:
        raise ValueError("Матрицы не могут быть пустыми!")

    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Размеры матриц не совпадают!")

    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def sub_matrix(A, B):
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def combine_matrix(A, B, C, D):
    n = len(A)

    E = [[0 for _ in range(n * 2)] for _ in range(n * 2)]

    for i in range(n):
        for j in range(n):
            E[i][j] = A[i][j]

    for i in range(n):
        for j in range(n, 2 * n):
            E[i][j] = B[i][j - n]

    for i in range(n, 2 * n):
        for j in range(n):
            E[i][j] = C[i - n][j]

    for i in range(n, 2 * n):
        for j in range(n, 2 * n):
            E[i][j] = D[i - n][j - n]

    return E


def recursive_matrix_multiply(A, B):
    n = len(A)

    if n <= 16:
        return classic_matrix_multiply(A, B)

    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    c11 = add_matrix(recursive_matrix_multiply(a11, b11), recursive_matrix_multiply(a12, b21))
    c12 = add_matrix(recursive_matrix_multiply(a11, b12), recursive_matrix_multiply(a12, b22))
    c21 = add_matrix(recursive_matrix_multiply(a21, b11), recursive_matrix_multiply(a22, b21))
    c22 = add_matrix(recursive_matrix_multiply(a21, b12), recursive_matrix_multiply(a22, b22))

    return combine_matrix(c11, c12, c21, c22)


def strassen_matrix_multiply(A, B):
    n = len(A)

    if n <= 16:
        return classic_matrix_multiply(A, B)

    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    p1 = strassen_matrix_multiply(add_matrix(a11, a22), add_matrix(b11, b22))
    p2 = strassen_matrix_multiply(add_matrix(a21, a22), b11)
    p3 = strassen_matrix_multiply(a11, sub_matrix(b12, b22))
    p4 = strassen_matrix_multiply(a22, sub_matrix(b21, b11))
    p5 = strassen_matrix_multiply(add_matrix(a11, a12), b22)
    p6 = strassen_matrix_multiply(sub_matrix(a21, a11), add_matrix(b11, b12))
    p7 = strassen_matrix_multiply(sub_matrix(a12, a22), add_matrix(b21, b22))

    c11 = add_matrix(sub_matrix(add_matrix(p1, p4), p5), p7)
    c12 = add_matrix(p3, p5)
    c21 = add_matrix(p2, p4)
    c22 = add_matrix(sub_matrix(add_matrix(p1, p3), p2), p6)

    return combine_matrix(c11, c12, c21, c22)




matrices = [
    ([[i for i in range(16)] for _ in range(16)], [[i for i in range(16)] for _ in range(16)]),
    ([[i for i in range(32)] for _ in range(32)], [[i for i in range(32)] for _ in range(32)]),
    ([[i for i in range(64)] for _ in range(64)], [[i for i in range(64)] for _ in range(64)]),
    ([[i for i in range(128)] for _ in range(128)], [[i for i in range(128)] for _ in range(128)]),
    ([[i for i in range(256)] for _ in range(256)], [[i for i in range(256)] for _ in range(256)])
]

algorithms = {
    'Classic Matrix Multiply': classic_matrix_multiply,
    'Recursive Matrix Multiply': recursive_matrix_multiply,
    'Strassen Matrix Multiply': strassen_matrix_multiply
}

results = []
for matrix_pair in matrices:
    matrix_results = {}
    for algo_name, algo_func in algorithms.items():
        elapsed_time = run_algorithm(algo_func, matrix_pair)
        matrix_results[algo_name] = elapsed_time
    results.append(matrix_results)

benchmarks = [f'Matrix {2**i}' for i in range(4, len(matrices) + 4)]
algos = list(algorithms.keys())
formatted_results = [[matrix_result.get(algo, '-') for algo in algos] for matrix_result in results]

def format_table(benchmarks, algos, results):
    all_values = [f"{bench}" for bench in benchmarks]
    all_values.append('Benchmark')
    all_values.extend([f"{alg}" for alg in algos])
    all_values.extend([str(value) for row in results for value in row])
    col_size = max(map(len, all_values))
    separator = "-" * ((col_size + 2) * (len(algos) + 1) + len(algos) + 2)
    header = f"| " + f"{'Benchmark':<{col_size}}" + f" | " + " | ".join(f"{alg:<{col_size}}" for alg in algos) + " |"
    print(header)
    print(separator)

    for benchmark, result in zip(benchmarks, results):
        string = f"| {benchmark:<{col_size}} | " + " | ".join(f"{value:<{col_size}}" for value in result) + " |"
        print(string)

if __name__ == '__main__':
    format_table(benchmarks, algos, formatted_results)

    print("\nДополнительная статистика:")

    algo_times = {algo: [] for algo in algos}
    for matrix_result in results:
        for algo in algos:
            algo_times[algo].append(matrix_result[algo])

    print(f"{'Алгоритм':<25} | {'Среднее':<8} | {'Ст. отклонение':<15} | {'Ср. геом.':<10}")
    print("-" * 70)

    for algo in algos:
        times = algo_times[algo]
        mean = statistics.mean(times)
        stdev = statistics.stdev(times) if len(times) > 1 else 0
        geo_mean = math.exp(sum(math.log(x) for x in times) / len(times)) if all(x > 0 for x in times) else 0

        print(f"{algo:<25} | {mean:.6f} | {stdev:.6f}        | {geo_mean:.6f}")

    print("\nСтатистика по размерам матриц:")
    print(f"{'Размер':<8} | {'Алгоритм':<25} | {'Среднее':<8} | {'Ст. отклонение':<15} | {'Ср. геом.':<10}")
    print("-" * 80)

    for size, benchmark in zip([16, 32, 64, 128, 256], benchmarks):
        for algo in algos:
            times = [res[algo] for res in results if f'Matrix {size}' in benchmark]
            if not times:
                continue

            mean = statistics.mean(times)
            stdev = statistics.stdev(times) if len(times) > 1 else 0
            geo_mean = math.exp(sum(math.log(x) for x in times) / len(times)) if all(x > 0 for x in times) else 0

            print(f"{size:<8} | {algo:<25} | {mean:.6f} | {stdev:.6f}        | {geo_mean:.6f}")

