from Algorithms.uninformed import*
from Algorithms.informed import*
from Models.zone import*

def compare_algorithms(graph, start, veiculos):
    results = {}
    # Calcular a prioridade de cada zona usando a função 'calculate_zone_priority'
    zone_priorities = calculate_zone_priority(graph)
    for goal in graph.nodes:
        if goal == start:
            continue  # Não calcular para o nó inicial
        # Armazenar os resultados para cada veículo
        algorithm_results_for_goal = {}
        for veiculo in veiculos:
            tipo = veiculo['type']
            
            # Aplicar os algoritmos para cada veículo
            bfs_results = bfs(graph, start, goal, [veiculo])
            dfs_results = dfs(graph, start, goal, [veiculo])
            ucs_results = uniform_cost_search(graph, start, goal, [veiculo])
            greedy_results = greedy_search(graph, start, goal, [veiculo])
            a_star_results = a_star_search(graph, start, goal, [veiculo])

            # Extrair o caminho e custo de cada algoritmo para o tipo de veículo
            bfs_path, bfs_cost = bfs_results.get(tipo, (None, float('inf')))
            dfs_path, dfs_cost = dfs_results.get(tipo, (None, float('inf')))
            ucs_path, ucs_cost = ucs_results.get(tipo, (None, float('inf')))
            greedy_path, greedy_cost = greedy_results.get(tipo, (None, float('inf')))
            a_star_path, a_star_cost = a_star_results.get(tipo, (None, float('inf')))
            
            # Dicionário com os resultados de todos os algoritmos para o veículo
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
                best_cost = float('inf')  # Definir best_cost mesmo quando não há resultados válidos
            # Guardar o melhor caminho para cada veículo
            algorithm_results_for_goal[tipo] = (best_path, best_cost)

        # Guardar os resultados para cada cidade (goal)
        results[goal] = algorithm_results_for_goal
    # Ordenar os resultados com base na prioridade das zonas
    sorted_results = dict(sorted(results.items(), key=lambda item: zone_priorities.get(item[0], 0), reverse=True))
    return sorted_results