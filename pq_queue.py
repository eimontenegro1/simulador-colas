from collections import defaultdict, deque

class PQQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, packet):
        self.queue.append(packet)

    def process(self):
        buckets = defaultdict(deque)
        for p in self.queue:
            buckets[p['prioridad']].append(p)

        result = []
        for prio in sorted(buckets.keys()):
            result.extend(buckets[prio])
        return result
