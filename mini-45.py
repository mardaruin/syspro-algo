import itertools
import random
from datetime import datetime

def generate_random_graph(n):
    return [[random.randint(1, 100) if i != j else float('inf') for j in range(n)] for i in range(n)]


def naive_tsp(graph):
    num_cities = len(graph)
    min_dist = float('inf')
    best = None

    start_time = datetime.now()

    for path in itertools.permutations(range(num_cities)):
        curr_dist = graph[path[-1]][path[0]]

        for i in range(len(path) - 1):
            curr_dist += graph[path[i]][path[i + 1]]

        if curr_dist < min_dist:
            min_dist = curr_dist
            best = path

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for naive tsp: {elapsed_time}")
    return best, min_dist


def bellman_held_karp(graph):
    n = len(graph)

    dp = [[float('inf')] * n for _ in range(1 << n)]

    dp[1][0] = 0

    start_time = datetime.now()

    for S in range(1 << n):
            binS = bin(S)
            for v in range(n):
                    #if S & (1 << v): # v in S
                        for w in range(n):
                            if not S & (1 << w) and graph[v][w] != 0:
                                mask = 1 << w
                                bin_mask = bin(mask)
                                S_with_v = S | mask
                                new_binS = bin(S_with_v)
                                dp[S_with_v][w] = min(dp[S][v] + graph[v][w], dp[S_with_v][w])

    result = float('inf')
    for v in range(1, n):
        result = min(result, dp[(1 << n) - 1][v] + graph[v][0])

    end_time = datetime.now()
    elapsed_time = end_time - start_time

    print(f"Elapsed time for Bellman Held tsp: {elapsed_time}")
    return result

if __name__ == "__main__":
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    rand_graph = generate_random_graph(100)

    print(naive_tsp(rand_graph))
    print(bellman_held_karp(rand_graph))