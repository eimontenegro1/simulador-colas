from collections import deque

class FIFOQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def process(self):
        return list(self.queue)

    def __str__(self):
        return str(list(self.queue))

