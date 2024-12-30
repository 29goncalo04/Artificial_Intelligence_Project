import heapq
from Algorithms.heuristics import*

def greedy_search(graph, start, goal):
    """
    Procura Gulosa.
    """
    # Calcula as heurísticas e armazena nos nós do grafo
    calculate_heuristics(graph, goal)

    # Fila de prioridade com base na heurística (h(n)): (heurística, custo acumulado, nó atual, caminho)
    pq = [(graph.nodes[start]['heuristic'], 0, start, [start])]
    visited = set()

    while pq:
        _, current_cost, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, current_cost

        # Adiciona os vizinhos na fila de prioridade
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                heapq.heappush(pq, (neighbor_heuristic, current_cost + edge_cost, neighbor, path + [neighbor]))
    
    return None, float('inf')



def a_star_search(graph, start, goal):
    """
    Algoritmo A* (retorna o caminho e o custo).
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
            return path, g  # Retorna o caminho e o custo total

        # Explorar os vizinhos
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                new_g = g + edge_cost
                neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                new_f = new_g + neighbor_heuristic
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
    
    return None, float('inf')  # Retorna custo infinito se nenhum caminho for encontrado