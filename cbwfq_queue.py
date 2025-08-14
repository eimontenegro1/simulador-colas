from collections import deque

class CBWFQQueue:
    def __init__(self):
        self.classes = {
            0: deque(),
            1: deque(),
            2: deque(),
            3: deque()
        }
        self.weights = {
            0: 4,
            1: 3,
            2: 2,
            3: 1
        }

    def enqueue(self, packet):
        prio = packet['prioridad']
        self.classes[prio].append(packet)

    def process(self):
        class_queues = {k: deque(v) for k, v in self.classes.items()}
        result = []
        while any(class_queues[k] for k in class_queues):
            for prio in sorted(class_queues.keys()):
                quantum = self.weights[prio]
                for _ in range(quantum):
                    if class_queues[prio]:
                        pkt = class_queues[prio].popleft()
                        result.append(pkt)
                    else:
                        break
        return result
