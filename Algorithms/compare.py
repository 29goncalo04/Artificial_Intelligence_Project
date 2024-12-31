from Algorithms.uninformed import*
from Algorithms.informed import*
from Models.zone import*

def compare_algorithms(graph, start):
    """
    Compara diferentes algoritmos de procura para encontrar o melhor caminho
    do nó inicial para todas as localidades com base no custo total.
    """
    results = {}

    # Calcular a prioridade de cada zona usando a função 'calculate_zone_priority'
    zone_priorities = calculate_zone_priority(graph)
    # for zone_id, priority in zone_priorities.items():
    #     print(f"Zona {zone_id}: Prioridade {priority}")

    for goal in graph.nodes:
        if goal == start:
            continue  # Não calcular para o nó inicial

        # Aplicar os algoritmos
        dfs_path, dfs_cost = dfs(graph, start, goal)
        bfs_path, bfs_cost = bfs(graph, start, goal)
        ucs_path, ucs_cost = uniform_cost_search(graph, start, goal)
        greedy_path, greedy_cost = greedy_search(graph, start, goal)
        a_star_path, a_star_cost = a_star_search(graph, start, goal)

        # Criar um dicionário com os resultados dos algoritmos
        all_results = {
            'DFS': (dfs_path, dfs_cost),
            'BFS': (bfs_path, bfs_cost),
            'UCS': (ucs_path, ucs_cost),
            'Greedy': (greedy_path, greedy_cost),
            'A*': (a_star_path, a_star_cost)
        }

        # Remover resultados inválidos (caminho None ou custo infinito)
        valid_results = {algo: result for algo, result in all_results.items() if result[0] and result[1] != float('inf')}

        # Escolher o melhor caminho com base no custo total
        if valid_results:
            best_algorithm = min(valid_results, key=lambda algo: valid_results[algo][1])
            best_path, best_cost = valid_results[best_algorithm]
        else:
            best_algorithm = None
            best_path = None

        # Guardar o resultado
        results[goal] = best_path, best_cost

        sorted_results = dict(sorted(results.items(), key=lambda item: zone_priorities.get(item[0], 0), reverse=True))

    return sorted_results