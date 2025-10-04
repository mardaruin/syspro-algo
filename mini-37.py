# Будем идти от листьев к корням, последовательно вычисляя
#   количество топологических сортировок для поддерева с данной корневой вершиной.
# Пусть f(node) = количество топологических сортировок на корневой вершине node.
# Тогда справедлива следующая формула:
#       f(node) = ∏(f(ci) * C(count[node] - 1 - (∑count[cj]), count[ci])), i=1,..,n, j=1,..,i-1
#           где c1, ... , cn - дети node,
#               count[node] - количество вершин в поддереве корневой вершины node
#               C(a, b) - биномиальный коэфф.
# Формула верна, т.к. для каждой топологической сортировки ребенка
#   нужно выбрать места среди всех потомков корневой вершины, что и делает биномиальный коэф.

from functools import lru_cache
from math import comb


class TreeNode:
    def __init__(self, value=None, count=1):
        self.value = value
        self.children = []
        self.count = count


@lru_cache(maxsize=None)
def calculate_f(node):
    """
    Возвращает количество топологических сортировок поддерева с корнем node.
    """
    if not node.children:
        return 1

    result = 1
    cumulative_sum = 0

    for ci in node.children:
        count_ci = ci.count
        binomial_coefficient = comb(node.count - 1 - cumulative_sum, count_ci)
        cumulative_sum += count_ci
        result *= calculate_f(ci) * binomial_coefficient

    return result

def make_simple_tree1():
    root = TreeNode(value="Root", count=5)
    child1 = TreeNode(value="Child1", count=2)
    child2 = TreeNode(value="Child2", count=2)
    grand_child1 = TreeNode(value="GrandChild1")
    grand_child2 = TreeNode(value="GrandChild2")

    root.children.extend([child1, child2])
    child1.children.append(grand_child1)
    child2.children.append(grand_child2)

    print(f"Количество топологических сортировок: {calculate_f(root)}")

def make_simple_tree2():
    root = TreeNode(value="Root", count=4)
    child1 = TreeNode(value="Child1", count=2)
    child2 = TreeNode(value="Child2")
    grand_child1 = TreeNode(value="GrandChild1")

    root.children.extend([child1, child2])
    child1.children.append(grand_child1)

    print(f"Количество топологических сортировок: {calculate_f(root)}")


make_simple_tree1()
make_simple_tree2()
