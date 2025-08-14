from collections import deque

class WFQQueue:
    def __init__(self):
        self.queues = {
            0: deque(),  # Alta prioridad
            1: deque(),  # Media prioridad
            2: deque(),  # Baja prioridad
            3: deque()   # Sin prioridad
        }
        self.weights = {
            0: 4,
            1: 3,
            2: 2,
            3: 1
        }
        self.order = [0, 1, 2, 3]

    def enqueue(self, packet):
        prioridad = packet['prioridad']
        if prioridad in self.queues:
            self.queues[prioridad].append(packet)
        else:
            self.queues[3].append(packet)

    def process(self):
        processed_packets = []
        total_packets = sum(len(q) for q in self.queues.values())

        # Mientras queden paquetes en alguna cola
        while len(processed_packets) < total_packets:
            for prio in self.order:
                weight = self.weights[prio]
                queue = self.queues[prio]

                count = 0
                # Procesamos hasta 'weight' paquetes, o hasta que la cola esté vacía
                while count < weight and queue:
                    packet = queue.popleft()
                    processed_packets.append(packet)
                    count += 1

                # Si la cola no está vacía, procesamos todos los paquetes restantes
                # antes de pasar a la siguiente prioridad, para evitar dispersión
                while queue:
                    packet = queue.popleft()
                    processed_packets.append(packet)

        return processed_packets


