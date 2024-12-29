import heapq

def bfs(graph, start, goal):
    """
    Busca em Largura (BFS).
    """
    queue = [(start, [start])]
    visited = set()

    while queue:
        current, path = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path

        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                queue.append((neighbor, path + [neighbor]))

    return None


def dfs(graph, start, goal):
    """
    Busca em Profundidade (DFS).
    """
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path

        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                stack.append((neighbor, path + [neighbor]))

    return None



def uniform_cost_search(graph, start, goal):
    """
    Busca de Custo Uniforme.
    Retorna apenas o caminho mais barato entre o nó inicial e o nó objetivo.
    """
    # Fila de prioridade: (custo acumulado, nó atual, caminho)
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        # Remove o nó com menor custo acumulado
        cost, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            return path

        # Adiciona vizinhos à fila de prioridade
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))
    return None