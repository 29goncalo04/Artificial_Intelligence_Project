import heapq
from Algorithms.heuristics import*

def greedy_search(graph, start, goal, veiculos):
    resultados = {}
    # Calcula as heurísticas e armazena nos nós do grafo
    calculate_heuristics(graph, goal)
    for veiculo in veiculos:
        tipo = veiculo['type']
        range_veiculo = veiculo['range']
        # Fila de prioridade com base na heurística (h(n)): (heurística, custo acumulado, nó atual, caminho)
        pq = [(graph.nodes[start]['heuristic'], 0, start, [start])]
        visited = set()
        while pq:
            _, current_cost, current, path = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                resultados[tipo] = (path, current_cost)  # Altere para uma tupla
                break
            # Adiciona os vizinhos na fila de prioridade
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
                    # Impede que o veículo avance se não tiver combustível suficiente para o próximo nó
                    if edge_cost > range_veiculo:
                        continue
                    neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                    # Coloca o vizinho na fila de prioridade com a heurística e o custo acumulado
                    heapq.heappush(pq, (neighbor_heuristic, current_cost + edge_cost, neighbor, path + [neighbor]))
        # Caso não encontre caminho
        if tipo not in resultados:
            resultados[tipo] = (None, float('inf'))  # Ajuste para uma tupla
    return resultados





def a_star_search(graph, start, goal, veiculos):
    resultados = {}
    # Calcula as heurísticas e armazena nos nós do grafo
    calculate_heuristics(graph, goal)
    for veiculo in veiculos:
        tipo = veiculo['type']
        range_veiculo = veiculo['range']
        # Fila de prioridade: (f, g, nó atual, caminho)
        pq = [(graph.nodes[start]['heuristic'], 0, start, [start])]
        visited = set()
        caminho_valido = False
        while pq:
            # Extrai o nó com o menor custo total estimado (f)
            _, g, current, path = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)
            # Verifica se chegou ao objetivo
            if current == goal:
                resultados[tipo] = (path, g)
                caminho_valido = True
                break
            # Explorar os vizinhos
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
                    new_g = g + edge_cost
                    # Impede que o veículo avance se não tiver range suficiente para o próximo nó
                    if edge_cost > range_veiculo:
                        continue
                    neighbor_heuristic = graph.nodes[neighbor]['heuristic']
                    new_f = new_g + neighbor_heuristic
                    # Adiciona o vizinho à fila de prioridade
                    heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
        # Caso não encontre caminho
        if tipo not in resultados or not caminho_valido:
            resultados[tipo] = (None, float('inf'))  # Ajuste para uma tupla
    return resultados