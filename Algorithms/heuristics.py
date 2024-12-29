import math

def calculate_heuristics(grafo, end_node):
    # Obter a localização do nó final
    end_location = grafo.nodes[end_node]['location']
    
    # Calcular heurísticas baseadas na distância euclidiana
    heuristics = {}
    for node_id in grafo.nodes:
        location = grafo.nodes[node_id]['location']

        # Distância euclidiana
        heuristic = math.sqrt((location[0] - end_location[0])**2 + (location[1] - end_location[1])**2)
        heuristics[node_id] = heuristic

    # Atualizar o grafo com as heurísticas
    for node_id in grafo.nodes:
        grafo.nodes[node_id]['heuristic'] = heuristics.get(node_id, None)