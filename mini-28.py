from collections import defaultdict


def find_recursive_components(graph):
    # Алгоритм Косараджу
    visited = set()
    order = []

    def dfs(u):
        stack = [(u, False)]
        while stack:
            node, processed = stack.pop()
            if processed:
                order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append((neighbor, False))

    for node in graph:
        if node not in visited:
            dfs(node)

    reversed_graph = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            reversed_graph[v].append(u)

    visited = set()
    sccs = []

    for node in reversed(order):
        if node not in visited:
            stack = [node]
            visited.add(node)
            component = []
            while stack:
                current = stack.pop()
                component.append(current)
                for neighbor in reversed_graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            sccs.append(component)

    return sccs


def analyze_functions(input_data):
    graph = {}
    for line in input_data.strip().split('\n'):
        if not line.strip():
            continue
        func, calls = line.split(':')
        func = func.strip()
        calls = [c.strip() for c in calls.split(',') if c.strip()]
        graph[func] = calls

    sccs = find_recursive_components(graph)

    largest_scc = max(sccs, key=len) if sccs else []

    recursive_funcs = set()
    for scc in sccs:
        if len(scc) > 1 or (len(scc) == 1 and scc[0] in graph.get(scc[0], [])):
            recursive_funcs.update(scc)

    result = {
        "largest_recursive_component": largest_scc,
        "recursive_funcs": recursive_funcs
    }
    return result


input_data = """
foo: bar, baz, qux
bar: baz, foo, bar
qux: qux
"""

result = analyze_functions(input_data)
print("Наибольшая рекурсивная компонента:", result["largest_recursive_component"])
print("Функции с рекурсивными вызовами:", result["recursive_funcs"])