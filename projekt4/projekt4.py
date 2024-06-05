import networkx as nx
import random

class Graph:
    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.graph = {vertex: [] for vertex in range(1, vertexes + 1)}
        self.matrix = [[0] * (vertexes + 1) for _ in range(1, vertexes + 2)]
        self.table = []

    def add_edge(self, start, end):
        self.graph[start].append(end)
        self.graph[end].append(start)
        self.matrix[start][end] = 1
        self.matrix[end][start] = 1
        self.table.append((start, end))
        self.table.append((end, start))

    def print_graph(self, representation="matrix"):
        if representation == "matrix":
            vertexes = sorted(self.graph.keys())
            print("  |", " ".join(str(vertex) for vertex in vertexes))
            print("--+" + "-" * (len(vertexes) * 2 - 1))
            for vertex in vertexes:
                row = ["1" if x in self.graph[vertex] else "0" for x in vertexes]
                print(f"{vertex} |", " ".join(row))
        elif representation == "list":
            for vertex, successors in self.graph.items():
                print(f"{vertex} |", " ".join(str(x) for x in successors))
        elif representation == "table":
            for start, end in self.table:
                print(f"{start} - {end}")
        else:
            print("Invalid graph representation.")

    def hamiltonian_cycle(self, representation="matrix"):
        n = self.vertexes
        Path = [-1] * (n + 1)
        visited = 0

        def is_valid_vertex(v, pos):
            if representation == "matrix":
                if self.matrix[Path[pos - 1]][v] == 0:
                    return False
            elif representation == "list":
                if v not in self.graph[Path[pos - 1]]:
                    return False
            elif representation == "table":
                if (Path[pos - 1], v) not in self.table:
                    return False
            if v in Path[:pos]:
                return False
            return True

        def hamiltonian(v):
            nonlocal visited
            visited += 1
            Path[visited] = v

            if visited == n:
                if representation == "matrix":
                    if self.matrix[Path[visited]][Path[1]] == 1:
                        return True
                elif representation == "list":
                    if Path[1] in self.graph[Path[visited]]:
                        return True
                elif representation == "table":
                    if (Path[visited], Path[1]) in self.table:
                        return True
                visited -= 1
                return False

            for i in range(1, n + 1):
                if is_valid_vertex(i, visited + 1):
                    if hamiltonian(i):
                        return True

            visited -= 1
            return False

        def hcycle():
            nonlocal visited
            Path[1] = 1
            visited = 0
            return hamiltonian(1)

        if hcycle():
            return Path[1:] + [Path[1]]
        else:
            return "Cykl Hamiltona nie istnieje"

    def find_eulerian_cycle(self, representation="matrix"):
        def dfs_euler(v):
            while True:
                if representation == "list":
                    if not self.graph[v]:
                        break
                    u = self.graph[v].pop()
                    self.graph[u].remove(v)
                elif representation == "matrix":
                    u = next((u for u, val in enumerate(self.matrix[v]) if val), None)
                    if u is None:
                        break
                    self.matrix[v][u] = 0
                    self.matrix[u][v] = 0
                elif representation == "table":
                    u = next((end for start, end in self.table if start == v), None)
                    if u is None:
                        break
                    self.table.remove((v, u))
                    self.table.remove((u, v))
                dfs_euler(u)
            eulerian_cycle.append(v)

        # Sprawdzenie warunków koniecznych dla istnienia cyklu Eulera
        if representation == "list":
            for vertices in self.graph.values():
                if len(vertices) % 2 != 0:
                    return "Graf nie ma cyklu Eulera (wierzchołek o nieparzystym stopniu)"
        elif representation == "matrix":
            for i in range(1, self.vertexes + 1):
                if sum(self.matrix[i]) % 2 != 0:
                    return "Graf nie ma cyklu Eulera (wierzchołek o nieparzystym stopniu)"
        elif representation == "table":
            degrees = {vertex: 0 for vertex in range(1, self.vertexes + 1)}
            for start, end in self.table:
                degrees[start] += 1
            if any(degree % 2 != 0 for degree in degrees.values()):
                return "Graf nie ma cyklu Eulera (wierzchołek o nieparzystym stopniu)"

        # Inicjalizacja
        eulerian_cycle = []
        start_vertex = next(iter(self.graph))  # Startujemy z dowolnego wierzchołka

        # Uruchomienie DFS
        dfs_euler(start_vertex)
        
        # Cykl jest w odwrotnej kolejności, więc odwracamy go
        eulerian_cycle.reverse()
        return eulerian_cycle

def generate_hamiltonian_graph(num_nodes, edge_saturation):
    """
    Generuje graf Hamiltona z określoną liczbą wierzchołków i nasyceniem krawędzi.
    """
    graph = nx.cycle_graph(num_nodes)  # Rozpocznij od grafu cyklu

    total_possible_edges = (num_nodes * (num_nodes - 1)) // 2
    target_num_edges = int((edge_saturation / 100) * total_possible_edges)
    edges_to_add = target_num_edges - graph.number_of_edges()

    # Losowo dodawaj krawędzie, aż osiągniesz pożądaną liczbę krawędzi
    while edges_to_add > 0:
        node1 = random.randint(0, num_nodes - 1)
        node2 = random.randint(0, num_nodes - 1)
        if node1 != node2 and not graph.has_edge(node1, node2):
            graph.add_edge(node1, node2)
            edges_to_add -= 1
    
    return graph

def generate_non_hamiltonian_graph(num_nodes, edge_saturation):
    """
    Generuje graf nie-Hamiltona z określoną liczbą wierzchołków i nasyceniem krawędzi.
    """
    graph = nx.complete_graph(num_nodes)  # Rozpocznij od grafu pełnego

    total_possible_edges = (num_nodes * (num_nodes - 1)) // 2
    num_edges_to_remove = total_possible_edges - int((edge_saturation / 100) * total_possible_edges)

    # Losowo usuwaj krawędzie, aż osiągniesz pożądaną liczbę krawędzi
    edges = list(graph.edges())
    edges_to_remove = random.sample(edges, num_edges_to_remove)
    graph.remove_edges_from(edges_to_remove)
    
    isolated_node = random.choice(list(graph.nodes()))  # Usuń węzeł, aby złamać możliwość ścieżki Hamiltona
    graph.remove_node(isolated_node)
    
    return graph
