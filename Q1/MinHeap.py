# custom class for a MinHeap data structure
# a MinHeap is represent by a binary tree where the parent of every node is lesser than either of it's children
# the binary tree is represented as a list where the index of the item indicates it position in the tree
# for a node a index i in the array, it has left child at index 2i + 1 and right child at index 2i + 2 and parent at index floor((i-1) / 2)
class MinHeap:
    # core MinHeap methods
    def __init__(self, items=None):
        self._arr = []
        if items is not None:
            self._arr = list(items)
            self._heapify()

    def __len__(self):
        return len(self._arr)

    def peek(self):
        if not self._arr:
            raise IndexError("peek from empty heap")
        return self._arr[0]

    def push(self, x):
        self._arr.append(x)
        self._sift_up(len(self._arr) - 1)

    def pop(self):
        if not self._arr:
            raise IndexError("pop from empty heap")
        last = self._arr.pop()
        if not self._arr:
            return last
        root = self._arr[0]
        self._arr[0] = last
        self._sift_down(0)
        return root

    # helper functions for the core MinHeap methods
    def _heapify(self):
        for i in range((len(self._arr) // 2) - 1, -1, -1):
            self._sift_down(i)

    # sift up moves a leaf upwards if its smaller than its parent
    def _sift_up(self, i):
        a = self._arr
        while i > 0:
            p = (i - 1) // 2
            if a[i] < a[p]:
                a[i], a[p] = a[p], a[i]
                i = p
            else:
                break

    # sift down moves a node downward it its larger than its children
    def _sift_down(self, i):
        a = self._arr
        n = len(a)
        while True:
            left = 2 * i + 1
            right = left + 1
            smallest = i
            if left < n and a[left] < a[smallest]:
                smallest = left
            if right < n and a[right] < a[smallest]:
                smallest = right
            if smallest != i:
                a[i], a[smallest] = a[smallest], a[i]
                i = smallest
            else:
                break