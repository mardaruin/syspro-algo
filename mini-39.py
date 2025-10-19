import random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = random.random() if priority is None else priority
        self.left = None
        self.right = None
        self.sum = key

def split(root, x):
    """splits on two treaps: left treap < x, right treap >= x"""
    if root is None:
        return None, None

    if root.key < x:
        l, r = split(root.right, x)
        root.right = l
        update_sum(root)
        return root, r
    else:
        l, r = split(root.left, x)
        root.left = r
        update_sum(root)
        return l, root

def merge(l, r):
    if not l:
        return r
    elif not r:
        return l

    elif r.priority > l.priority:
        l.right = merge(l.right, r)
        update_sum(l)
        return l
    else:
        r.left = merge(l, r.left)
        update_sum(r)
        return r

def insert(root, key):
    new_node = TreapNode(key)
    if not root:
        return new_node
    l, r = split(root, key)
    return merge(merge(l, new_node), r)

def remove(root, key):

    if root is None:
        return None

    if root.key == key:
        return merge(root.left, root.right)
    elif root.key < key:
        root.right = remove(root.right, key)
    else:
        root.left = remove(root.left, key)
    update_sum(root)
    return root

def update_sum(node):
    if node is None:
        return
    node.sum = node.key
    if node.left:
        node.sum += node.left.sum
    if node.right:
        node.sum += node.right.sum

def range_sum(root, from_key, to_key):
    left, rest = split(root, from_key)
    part_1, part_2 = split(rest, to_key + 1)
    merged = merge(left, rest)
    result = part_1.sum if part_1 else 0
    return result

root = None
arr = [1, 2, 3, 4, 5]
for num in arr:
    root = insert(root, num)

print("Сумма элементов от 0 до 2:", range_sum(root, 0, 2))   # 3

root = None
arr = [7, 10, 12, 20, 40]
for num in arr:
    root = insert(root, num)

print("Сумма элементов от 1 до 3:", range_sum(root, 12, 20))   # 32


root = None
arr = [5, 7, 10, 100, 135]
for num in arr:
    root = insert(root, num)
print("Сумма элементов от 2 до 4:", range_sum(root, 100, 139))   # 235
