import heapq
from Algorithms.heuristics import*

def greedy_search(graph, start, goal):
    """
    Busca Gulosa.
    """
    # Calcula as heurísticas e armazena nos nós do grafo
    calculate_heuristics(graph, goal)

    # Fila de prioridade com base na heurística (h(n)): (heurística, nó atual, caminho)
    pq = [(graph.nodes[start]['heuristic'], start, [start])]
    visited = set()

    while pq:
        _, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path

        # Adiciona os vizinhos na fila de prioridade
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                heapq.heappush(pq, (neighbor_heuristic, neighbor, path + [neighbor]))
    return None


def a_star_search(graph, start, goal):
    """
    Algoritmo A* (retorna apenas o caminho).
    """
    # Calcula as heurísticas e armazena nos nós do grafo
    calculate_heuristics(graph, goal)

    # Fila de prioridade com base no custo total estimado (f = g + h)
    pq = [(graph.nodes[start]['heuristic'], 0, start, [start])]  # (f, g, nó atual, caminho)
    visited = set()

    while pq:
        _, g, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path

        # Explorar os vizinhos
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                new_g = g + edge_cost
                neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                new_f = new_g + neighbor_heuristic
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
    return None