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


def get_critical_time(graph, path):
    last_zone = path[-1]
    zone = graph.nodes[last_zone]
    return zone.get('critical_time', float('inf'))


def get_population(graph, path):
    last_zone = path[-1]
    zone = graph.nodes[last_zone]
    return zone.get('population', None)


def calculate_zone_priority(graph, weight_priority=0.7, weight_population=0.3):
    zones = get_all_zones(graph)

    # Encontrar o maior valor de população
    max_population = max(zone['population'] for zone in zones)

    # Calcular o grau de prioridade para cada zona
    zone_priorities = {}
    for zone in zones:
        priority = zone['priority']
        population = zone['population']

        population_scaled = population / max_population

        # Calcular o grau de prioridade usando pesos
        zone_priority = (weight_priority * priority) + (weight_population * population_scaled)

        # Armazenar o resultado no dicionário
        zone_priorities[zone['id']] = zone_priority

    return zone_priorities