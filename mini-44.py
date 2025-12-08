from distutils.command.build import build


class Node:
    def __init__(self, val, par=None):
        self.value = val
        self.parent = par

class ListNode:
    def __init__(self, node):
        self.node = node
        self.next = None

class PersistentQueue:
    def __init__(self):
        self.first = None
        self.last = None
        self.list_ptr = None
        self.build_list_ptr = None

    def push(self, val):
        node = Node(val, self.last)
        queue = PersistentQueue()
        if self.first is None:
            queue.first = node
        else:
            queue.first = self.first
        queue.last = node
        queue.list_ptr = self.list_ptr
        queue.build_list_ptr = self.build_list_ptr

        if self.build_list_ptr is None:
            int_count = self.count_intermediate_nodes()
            if int_count > 0 and 2 * len(self.get_list()) <= int_count:
                new_list_node = ListNode(node.parent)
                new_list_node.next = None
                queue.build_list_ptr = new_list_node

        elif self.build_list_ptr is not None:
            prev_build_list = self.build_list_ptr
            new_list_node = ListNode(prev_build_list.node.parent)
            new_list_node.next = prev_build_list
            queue.build_list_ptr = new_list_node

        return queue

    def pop(self):
        if self.first is None:
            raise ValueError("Queue is empty")
        queue = PersistentQueue()
        queue.last = self.last
        queue.list_ptr = self.list_ptr
        queue.build_list_ptr = self.build_list_ptr

        if self.list_ptr is None:
            int_count = self.count_intermediate_nodes()
            if int_count >= 1:
                if self.build_list_ptr is not None:
                    last_build_list_node = self.build_list_ptr
                    queue.list_ptr = last_build_list_node
                    queue.first = last_build_list_node
        else:
            queue.list_ptr = queue.list_ptr.next


        return queue


    def count_intermediate_nodes(self):
        c = 0
        node = self.last
        while node != self.first:
            c += 1
            node = node.parent
        return c

    def get_list(self):
        result = []
        curr = self.list_ptr
        if self.list_ptr is not None:
            curr = curr.next
        while curr is not None:
            result.append(curr.node.value)
            curr = curr.next
        return result


    def get_queue(self):
        node = self.last
        result = []
        if (self.first is None) or (self.last is None):
            return result
        while node != self.first and node is not None:
            result.append(node.value)
            node = node.parent
        result.append(self.first.value)

        return result


if __name__ == "__main__":
    q = PersistentQueue()
    q = q.push('A')
    q = q.push('B')
    q = q.push('C')
    print(q.get_queue())
    q = q.pop()
    print(q.get_list())