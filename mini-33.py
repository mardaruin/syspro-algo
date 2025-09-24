from typing import List

class Solution:
    def scheduleTasks(self, tasks: List[tuple]):
        """
        :param tasks: Список кортежей вида (штраф, дедлайн)
        :return: Расписание заданий с минимизацией штрафов
        """
        n = max(task[1] for task in tasks)
        parent = [i for i in range(n + 1)]
        rank = [0] * (n + 1)
        fine = 0

        def find(node):
            if node != parent[node]:
                parent[node] = find(parent[node])
            return parent[node]

        def union(u, v):
            pu, pv = find(u), find(v)
            if pu != pv:
                #if rank[pu] > rank[pv]:
                    #parent[pv] = pu
                #elif rank[pu] < rank[pv]:
                parent[pu] = pv
                #else:
                    #parent[pv] = pu
                rank[pu] += 1
                return True
            return False

        tasks.sort(reverse=True)
        schedule = [-1] * n

        for idx, (penalty, deadline) in enumerate(tasks):
            found_slot = False
            for t in reversed(range(1, deadline + 1)):
                if find(t) == t:
                    found_slot = True
                    schedule[t - 1] = idx
                    union(t, t-1)
                    break
            if not found_slot:
                fine += penalty


        return f"Hi, this is yout task schedule (ind): {schedule},\n then just relax, your fine will be {fine}"

solution = Solution()
tasks = [(10, 3), (8, 1), (5, 2), (3, 2), (3, 1)]  # штрафы и дедлайны соответственно
print(solution.scheduleTasks(tasks))