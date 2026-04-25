import heapq


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0  # menjaga stabilitas (FIFO untuk prioritas sama)

    def is_empty(self):
        return len(self._heap) == 0

    def enqueue(self, item, priority):
        """
        priority kecil = lebih dulu diproses (min-heap)
        """
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Priority Queue is empty")

        priority, _, item = heapq.heappop(self._heap)
        return item

    def peek(self):
        if self.is_empty():
            return None
        priority, _, item = self._heap[0]
        return item

    def size(self):
        return len(self._heap)

    def clear(self):
        self._heap.clear()
        self._counter = 0

    def get_all(self):
        """
        Return list dalam urutan prioritas (tanpa merusak heap)
        """
        return [item for (priority, _, item) in sorted(self._heap)]

    def get_with_priority(self):
        """
        Untuk visual: return (item, priority)
        """
        return [(item, priority) for (priority, _, item) in sorted(self._heap)]