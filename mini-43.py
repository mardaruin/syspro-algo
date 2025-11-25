class Node:
    def __init__(self, alive=False, left=None, right=None):
        self.alive = alive
        self.left = left
        self.right = right

class PersistentSegmentTree:
    def __init__(self, nums):
        self.nums = nums
        self.n = len(nums)
        self.sorted_idx = sorted(range(self.n), key=lambda i: -nums[i])
        self.roots = [self.build(0, self.n - 1)]

        for i in range(self.n):
            orig_pos = self.sorted_idx[i]
            next_root = self.revive(self.roots[-1], 0, self.n - 1, orig_pos)
            self.roots.append(next_root)

    def build(self, l, r):
        if l == r:
            return Node(alive=False)
        mid = (l + r) // 2
        left = self.build(l, mid)
        right = self.build(mid + 1, r)
        return Node(alive=(left.alive or right.alive), left=left, right=right)

    def revive(self, root, l, r, index):
        if l == r:
            return Node(alive=True)
        mid = (l + r) // 2
        if index <= mid:
            new_left = self.revive(root.left, l, mid, index)
            new_right = root.right
        else:
            new_left = root.left
            new_right = self.revive(root.right, mid + 1, r, index)
        return Node(alive=(new_left.alive or new_right.alive), left=new_left, right=new_right)

    def _gte(self, root, vl, vr, l, r):
        if l > r:
            return 0
        if l == vl and r == vr:
            return root.alive
        mid = (vl + vr) // 2
        total = 0
        if l <= mid:
            total += self._gte(root.left, vl, mid, l, min(r, mid))
        if r > mid:
            total += self._gte(root.right, mid + 1, vr, max(l, mid + 1), r)
        return total

    def gte(self, l, r, k):
        version = next((i for i, idx in enumerate(self.sorted_idx) if nums[idx] < k), self.n)
        root = self.roots[min(version, self.n)]
        return self._gte(root, 0, self.n - 1, l, r)



nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
pst = PersistentSegmentTree(nums)

assert(pst.gte(2, 7, 4) == 3)
assert(pst.gte(0, 3, 5) == 0)