def get_all_zones(graph):
    zones = []
    for node in graph.nodes:
        zone = graph.nodes[node]
        zones.append({
            'id': node,
            'priority': zone['priority'],
            'population': zone['population'],
            'critical_time': zone['critical_time'],
            'location': zone['location']
        })
    return zones



def calculate_zone_priority(graph, weight_priority=0.7, weight_population=0.3):
    """
    Calcula o grau de prioridade para cada zona usando 'priority' e 'population'.
    
    Args:
        zones (list): Lista de zonas com 'priority' e 'population'.
        weight_priority (float): Peso da prioridade (default = 0.7).
        weight_population (float): Peso da população (default = 0.3).
    
    Returns:
        dict: Um dicionário com o ID da zona e o grau de prioridade.
    """

    zones = get_all_zones(graph)

    # Encontrar o maior valor de população para normalização
    max_population = max(zone['population'] for zone in zones)

    # Calcular o grau de prioridade para cada zona
    zone_priorities = {}
    for zone in zones:
        priority = zone['priority']
        population = zone['population']

        # Normalizar a população
        population_scaled = population / max_population

        # Calcular o grau de prioridade usando pesos
        zone_priority = (weight_priority * priority) + (weight_population * population_scaled)

        # Armazenar o resultado no dicionário
        zone_priorities[zone['id']] = zone_priority

    return zone_priorities