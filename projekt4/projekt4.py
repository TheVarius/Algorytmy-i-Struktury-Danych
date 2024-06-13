import copy
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = {vertex: [] for vertex in range(vertices)}
        self.matrix = [[0] * vertices for _ in range(vertices)]
        self.table = []
        self.degrees = {vertex: 0 for vertex in range(vertices)}

    def add_edge(self, start, end):
        self.graph[start].append(end)
        self.graph[end].append(start)
        self.matrix[start][end] = 1
        self.matrix[end][start] = 1
        self.table.append((start, end))
        self.table.append((end, start))
        self.degrees[start] += 1
        self.degrees[end] += 1

    def remove_edge(self, u, v):
        self.matrix[u][v] = 0
        self.matrix[v][u] = 0
        self.graph[u].remove(v)
        self.graph[v].remove(u)
        self.table.remove((u, v))
        self.table.remove((v, u))
        self.degrees[u] -= 1
        self.degrees[v] -= 1

    def print_graph(self, representation="matrix"):
        if representation == "matrix":
            for row in self.matrix:
                print(row)
        elif representation == "list":
            for vertex, successors in self.graph.items():
                print(f"{vertex} |", " ".join(str(x) for x in successors))
        elif representation == "table":
            for start, end in self.table:
                print(f"{start} - {end}")
        else:
            print("Invalid graph representation.")

    def export_graph(self, filename="graph.png"):
        G = nx.Graph()
        for vertex in range(self.vertices):
            G.add_node(vertex)
        for start, end in self.table:
            G.add_edge(start, end)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', node_size=700, font_size=15)
        plt.savefig(filename)
        plt.close()

    def is_connected(self):
        visited = [False] * self.vertices
        stack = [0]
        visited[0] = True

        while stack:
            current = stack.pop()
            for i in range(self.vertices):
                if self.matrix[current][i] and not visited[i]:
                    stack.append(i)
                    visited[i] = True

        return all(visited)

    def euler(self):
        if not self.is_connected() or any(degree % 2 != 0 for degree in self.degrees.values()):
            print("No Euler cycle")
            return

        graph_copy = copy.deepcopy(self.matrix)
        cycle = []
        stack = [0]

        def dfs(v):
            for u in range(self.vertices):
                if graph_copy[v][u]:
                    graph_copy[v][u] = graph_copy[u][v] = 0
                    dfs(u)
            cycle.append(v)

        dfs(0)
        cycle.reverse()

        print("Euler cycle exists")
        print("Cycle:", cycle)

    def create_hamiltonian_cycle(self):
        vertices = list(range(self.vertices))
        random.shuffle(vertices)
        for i in range(len(vertices)):
            self.add_edge(vertices[i], vertices[(i + 1) % self.vertices])

    def create_additional_edges(self, target_edges):
        current_edges = sum(sum(row) for row in self.matrix) // 2
        edges_to_add = target_edges - current_edges

        while edges_to_add > 0:
            u, v = random.sample(range(self.vertices), 2)
            if self.matrix[u][v] == 0:
                self.add_edge(u, v)
                edges_to_add -= 1

    def ensure_even_degrees(self):
        for i in range(self.vertices):
            if self.degrees[i] % 2 != 0:
                for j in range(self.vertices):
                    if self.degrees[j] % 2 != 0 and i != j and self.matrix[i][j] == 0:
                        self.add_edge(i, j)
                        break

    def create_graph_with_saturation(self, saturation):
        self.create_hamiltonian_cycle()
        max_edges = self.vertices * (self.vertices - 1) // 2
        target_edges = int(max_edges * saturation)
        self.create_additional_edges(target_edges)
        self.ensure_even_degrees()

    def create_non_hamiltonian_graph(self, saturation):
        self.create_graph_with_saturation(saturation)
        isolated_vertex = random.choice(range(self.vertices))
        for i in range(self.vertices):
            if self.matrix[isolated_vertex][i] == 1:
                self.remove_edge(isolated_vertex, i)
        self.degrees[isolated_vertex] = 0

    def find_hamiltonian_cycle(self):
        n = self.vertices
        Path = [-1] * n
        Path[0] = 0

        def is_valid_vertex(v, pos):
            if not self.matrix[Path[pos - 1]][v]:
                return False
            if v in Path[:pos]:
                return False
            return True

        def hamiltonian(pos):
            if pos == n:
                return self.matrix[Path[pos - 1]][Path[0]] == 1

            for v in range(1, n):
                if is_valid_vertex(v, pos):
                    Path[pos] = v
                    if hamiltonian(pos + 1):
                        return True
                    Path[pos] = -1

            return False

        if hamiltonian(1):
            print("Hamiltonian cycle exists")
            print("Cycle:", Path + [Path[0]])
        else:
            print("No Hamiltonian cycle")
