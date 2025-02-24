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
    return [x - y for x, y in zip(A, B)]

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

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    c11 = add_matrix(recursive_matrix_multiply(a11, b11), recursive_matrix_multiply(a12, b21))
    c12 = add_matrix(recursive_matrix_multiply(a11, b12), recursive_matrix_multiply(a12, b22))
    c21 = add_matrix(recursive_matrix_multiply(a21, b11), recursive_matrix_multiply(a22, b21))
    c22 = add_matrix(recursive_matrix_multiply(a21, b12), recursive_matrix_multiply(a22, b22))

    return combine_matrix(c11, c12, c21, c22)


def strassen_matrix_multiply(A, B):
    n = len(A)

    if n <= 42:
        return recursive_matrix_multiply(A, B)

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

A = [[1, 2, 3, 5], [4, 5, 6, 5], [7, 8, 9, 5], [5, 5, 5, 5]]
B = [[11, 12, 13, 33], [14, 15, 16, 33], [17, 18, 19, 33], [33, 33, 33, 33]]

print(classic_matrix_multiply(A, B))
print(recursive_matrix_multiply(A, B))
print(strassen_matrix_multiply(A, B))