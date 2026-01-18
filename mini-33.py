from typing import List

class Node:
    def __init__(self, parent, left, ind):
        self.next_left = left
        self.parent = parent
        self.rank = 0
        self.ind = ind

class Solution:
    def scheduleTasks(self, tasks: List[tuple]):
        """
        :param tasks: Список кортежей вида (штраф, дедлайн)
        :return: Расписание заданий с минимизацией штрафов
        """
        n = max(task[1] for task in tasks)
        fine = 0

        nodes = [Node(i, i, i) for i in range(n + 1)]

        def find(node):
            if nodes[node].ind != nodes[node].parent:
                nodes[node].parent = find(nodes[node].parent)
            return nodes[node].parent

        def union(u, v):
            pu, pv = nodes[find(u)], nodes[find(v)]
            if pu != pv:
                if pu.rank > pv.rank:
                    pv.parent = pu
                    if pu.next_left > pv.next_left:
                        pu.next_left = pv.next_left
                elif pu.rank < pv.rank:
                    pu.parent = pv
                    if pu.next_left < pv.next_left:
                        pv.next_left = pu.next_left
                else:
                    pv.parent = pu.parent
                    if pu.next_left > pv.next_left:
                        pu.next_left = pv.next_left
                    pu.rank += 1

                return True
            return False

        def get_next_left(node_ind):
            return nodes[find(node_ind)].next_left

        #tasks.sort(reverse=True)
        schedule = [-1] * n

        for idx, (penalty, deadline) in enumerate(tasks):
            found_slot = False
            next_left = get_next_left(deadline)
            if next_left is not None and next_left >= 1 and next_left <= deadline:
                found_slot = True
                schedule[next_left - 1] = idx
                union(next_left, next_left - 1)
            if not found_slot:
                fine += penalty


        return f"Hi, this is your task schedule (ind): {schedule},\n then just relax, your fine will be {fine}"

solution = Solution()
tasks = [(10, 3), (8, 1), (5, 2), (3, 2), (3, 1)]  # штрафы и дедлайны соответственно
print(solution.scheduleTasks(tasks))