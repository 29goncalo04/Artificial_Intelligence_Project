import heapq

def bfs(graph, start, goal, veiculos):
    resultados = {}
    for veiculo in veiculos:
        tipo = veiculo['type']
        range_veiculo = veiculo['range']
        queue = [(start, [start], 0)]  # (nó atual, caminho, custo acumulado)
        visited = set()
        while queue:
            current, path, cost = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                resultados[tipo] = (path, cost)
                break
            for neighbor in graph.neighbors(current):
                edge = graph[current][neighbor]
                # Verifica se a rota está bloqueada ou se o veículo não pode usá-la
                if (
                    neighbor not in visited
                    and not edge.get('blocked', False)
                    and not (
                        tipo == 'camião' and edge['type'] == 'air'
                    )
                ):
                    edge_cost = edge['distance']
                    # Verifica se o veículo tem combustível suficiente para avançar até o próximo nó
                    if edge_cost <= range_veiculo:
                        queue.append((neighbor, path + [neighbor], cost + edge_cost))
        # Caso não encontre caminho
        if tipo not in resultados:
            resultados[tipo] = (None, float('inf'))  # Ajuste para uma tupla
    return resultados


def dfs(graph, start, goal, veiculos):
    resultados = {}
    for veiculo in veiculos:
        tipo = veiculo['type']
        range_veiculo = veiculo['range']
        stack = [(start, [start], 0)]  # (nó atual, caminho, custo acumulado)
        visited = set()
        while stack:
            current, path, cost = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                resultados[tipo] = (path, cost)
                break
            for neighbor in graph.neighbors(current):
                edge = graph[current][neighbor]
                # Verifica se a rota está bloqueada ou se o veículo não pode usá-la
                if (
                    neighbor not in visited
                    and not edge.get('blocked', False)
                    and not (
                        tipo == 'camião' and edge['type'] == 'air'
                    )
                ):
                    edge_cost = edge['distance']
                    # Verifica se o veículo tem combustível suficiente para avançar até o próximo nó
                    if edge_cost <= range_veiculo:
                        stack.append((neighbor, path + [neighbor], cost + edge_cost))
        # Caso não encontre caminho
        if tipo not in resultados:
            resultados[tipo] = (None, float('inf'))  # Ajuste para uma tupla
    return resultados


def uniform_cost_search(graph, start, goal, veiculos):
    resultados = {}
    for veiculo in veiculos:
        tipo = veiculo['type']
        range_veiculo = veiculo['range']
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
                resultados[tipo] = (path, cost)
                break
            # Adiciona vizinhos à fila de prioridade
            for neighbor in graph.neighbors(current):
                edge = graph[current][neighbor]
                # Verifica se a rota está bloqueada ou se o veículo não pode usá-la
                if (
                    neighbor not in visited
                    and not edge.get('blocked', False)
                    and not (
                        tipo == 'camião' and edge['type'] == 'air'
                    )
                ):
                    edge_cost = edge['distance']
                    # Verifica se o veículo tem combustível suficiente para avançar até o próximo nó
                    if edge_cost <= range_veiculo:
                        heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))
        # Caso não encontre caminho
        if tipo not in resultados:
            resultados[tipo] = (None, float('inf'))  # Ajuste para uma tupla
    return resultados