from collections import deque

class WFQQueue:
    def __init__(self):
        self.queues = {
            0: deque(),  # Alta prioridad
            1: deque(),
            2: deque(),
            3: deque()   # Baja prioridad
        }
        self.weights = {
            0: 4,
            1: 3,
            2: 2,
            3: 1
        }
        self.order = [0, 1, 2, 3]  # Orden de prioridades

    def enqueue(self, packet):
        prioridad = packet['prioridad']
        if prioridad in self.queues:
            self.queues[prioridad].append(packet)
        else:
            self.queues[3].append(packet)  # Default sin prioridad conocida

    def process(self):
        processed_packets = []
        total_packets = sum(len(q) for q in self.queues.values())
        
        while len(processed_packets) < total_packets:
            for prio in self.order:
                weight = self.weights[prio]
                queue = self.queues[prio]

                # Procesamos 'weight' paquetes si están disponibles
                for _ in range(weight):
                    if queue:
                        packet = queue.popleft()
                        processed_packets.append(packet)

        return processed_packets
