import heapq

def bfs(graph, start, goal):
    """
    Procura em Largura (BFS) que retorna o caminho e o custo total.
    """
    queue = [(start, [start], 0)]  # (nó atual, caminho, custo acumulado)
    visited = set()

    while queue:
        current, path, cost = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, cost  # Retorna o caminho e o custo total

        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                queue.append((neighbor, path + [neighbor], cost + edge_cost))

    return None, float('inf')  # Retorna custo infinito se nenhum caminho for encontrado


def dfs(graph, start, goal):
    """
    Procura em Profundidade (DFS) que retorna o caminho e o custo total.
    """
    stack = [(start, [start], 0)]  # (nó atual, caminho, custo acumulado)
    visited = set()

    while stack:
        current, path, cost = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, cost  # Retorna o caminho e o custo total

        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                stack.append((neighbor, path + [neighbor], cost + edge_cost))

    return None, float('inf')  # Retorna custo infinito se nenhum caminho for encontrado



def uniform_cost_search(graph, start, goal):
    """
    Procura de Custo Uniforme.
    Retorna o caminho mais barato e o custo total entre o nó inicial e o nó objetivo.
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
            return path, cost  # Retorna o caminho e o custo total

        # Adiciona vizinhos à fila de prioridade
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and not graph[current][neighbor]['blocked']:
                edge_cost = graph[current][neighbor]['distance']
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))

    return None, float('inf')  # Retorna custo infinito se nenhum caminho for encontrado