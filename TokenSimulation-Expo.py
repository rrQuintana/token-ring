import threading
import time

class Node(threading.Thread):
    def __init__(self, node_id, token_ring):
        threading.Thread.__init__(self)
        self.node_id = node_id
        self.token_ring = token_ring
        self.running = True

    def run(self):
        while self.running:
            if self.token_ring.get_token() == self.node_id:
                print(f"Nodo {self.node_id} tiene el token.")
                time.sleep(1)  # Simula tiempo de procesamiento
                
                next_node = self.find_next_active_node()
                # Simular el envío de su ID al siguiente nodo
                self.token_ring.collect_ids(self.node_id)
                self.token_ring.set_token(next_node)
                time.sleep(1)  # Espera antes de volver a recibir el token

    def stop_node(self):
        self.running = False
        print(f"Nodo {self.node_id} ha caido.")
        self.token_ring.initiate_leader_election()

    def find_next_active_node(self):
        next_index = (self.node_id + 1) % len(self.token_ring.nodes)
        while not self.token_ring.nodes[next_index].running:
            next_index = (next_index + 1) % len(self.token_ring.nodes)
        return next_index

class TokenRing:
    def __init__(self, num_nodes):
        self.token = 0
        self.nodes = [Node(i, self) for i in range(num_nodes)]
        self.active_ids = []
        self.collected_ids = []

    def get_token(self):
        return self.token

    def set_token(self, node_id):
        self.token = node_id

    def start_all(self):
        for node in self.nodes:
            node.start()

    def stop_node(self, node_id):
        self.nodes[node_id].stop_node()
        self.initiate_leader_election()

    def collect_ids(self, node_id):
        self.collected_ids.append(node_id)
        if len(self.collected_ids) == len(self.active_ids):
            self.determine_leader()

    def initiate_leader_election(self):
        self.active_ids = [node.node_id for node in self.nodes if node.running]
        self.collected_ids = []
        if self.active_ids:
            self.set_token(self.active_ids[0])  # Comenzar el proceso de elección desde el primer nodo activo

    def determine_leader(self):
        if self.collected_ids:
            new_leader = max(self.collected_ids)
            print(f"El nuevo lider es el nodo {new_leader}.")
            self.set_token(new_leader)

num_nodes = 5
token_ring = TokenRing(num_nodes)
token_ring.start_all()

time.sleep(5)
print("Simulando la caida del nodo 2.")
token_ring.stop_node(2)
