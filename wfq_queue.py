import heapq

class WFQQueue:
    def __init__(self):
        self.queue = []
        self.virtual_time = 0.0
        self.last_finish_time = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
        # 💡 Nuevo: Agregamos un contador para desempatar paquetes
        self.counter = 0

    def enqueue(self, packet):
        weights = {0: 4, 1: 3, 2: 2, 3: 1}
        peso = weights.get(packet['prioridad'], 1)

        start_time = max(self.virtual_time, self.last_finish_time[packet['prioridad']])
        finish_time = start_time + (1 / peso)

        packet['start_time'] = start_time
        packet['finish_time'] = finish_time
        packet['peso'] = peso

        self.last_finish_time[packet['prioridad']] = finish_time

        # 💡 La corrección: Encolamos una tupla de 3 elementos:
        # (finish_time, contador, packet)
        # heapq usará 'finish_time' para ordenar y 'counter' para desempatar si son iguales
        heapq.heappush(self.queue, (finish_time, self.counter, packet))
        # Incrementamos el contador para que cada paquete tenga un ID único de encolado
        self.counter += 1

    def process(self):
        processed_packets = []
        while self.queue:
            # 💡 La corrección: Extraemos la tupla completa
            finish_time, counter, packet = heapq.heappop(self.queue)
            
            self.virtual_time = max(self.virtual_time, finish_time)
            
            processed_packets.append(packet)
            
        return processed_packets