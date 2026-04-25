class Queue:
    def __init__(self, capacity=None):
        self._data = []
        self._capacity = capacity

    def is_empty(self):
        return len(self._data) == 0

    def is_full(self):
        if self._capacity is None:
            return False
        return len(self._data) >= self._capacity

    def enqueue(self, item):
        if self.is_full():
            raise Exception("Queue is full")
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self._data.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def get_all(self):
        return list(self._data)