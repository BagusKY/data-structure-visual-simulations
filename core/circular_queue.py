class CircularQueue:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self._capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def enqueue(self, item):
        if self.is_full():
            raise Exception("Circular Queue is full")

        self._rear = (self._rear + 1) % self._capacity
        self._data[self._rear] = item
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Circular Queue is empty")

        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1

        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._data[self._front]

    def size(self):
        return self._size

    def clear(self):
        self._data = [None] * self._capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    def get_all(self):
        """Return elements in logical order (front → rear)"""
        result = []
        index = self._front

        for _ in range(self._size):
            result.append(self._data[index])
            index = (index + 1) % self._capacity

        return result

    def get_raw(self):
        """Return raw internal array (for advanced visualization)"""
        return list(self._data)

    def get_front_index(self):
        return self._front

    def get_rear_index(self):
        return self._rear