import networkx as nx
import random

def generate_weather_conditions():
    weather_conditions = ["sol", "chuva", "neve", "vento", "tempestade"]
    return random.choice(weather_conditions)

def generate_blocked_status(connection, weather):
    if weather == 'tempestade': 
        return True
    elif connection['type'] == "road" and weather != 'sol':
        return random.random() <= 0.05  # 5% de chance de estar bloqueada
    else:
        return False

def create_graph(data):
    graph = nx.DiGraph()  # Grafo direcionado

    # Adicionar os nós com atributos
    for zone in data['zones']:
        graph.add_node(
            zone['id'],
            priority=zone['priority'],
            population=zone['population'],
            critical_time=zone['critical_time'],
            location=tuple(zone['location'])  # Converter a lista para tupla
        )

    # Adicionar as arestas com atributos
    for connection in data['connections']:
        weather=generate_weather_conditions()
        blocked_status = generate_blocked_status(connection, weather)
        graph.add_edge(
            connection['from'],
            connection['to'],
            distance=connection['distance'],
            type=connection['type'],
            blocked=blocked_status,
            weather=weather
        )
        # Adicionar a aresta reversa automaticamente
        graph.add_edge(
            connection['to'],
            connection['from'],
            distance=connection['distance'],
            type=connection['type'],
            blocked=blocked_status,
            weather=weather
        )
    return graph



def has_air_connection(graph, path):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        edge_type = graph[u][v].get('type')
        if edge_type == "air":
            return True
    return False

def has_road_connection(graph, path):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        edge_type = graph[u][v].get('type')
        if edge_type == "road":
            return True
    return False

def has_blocked_road(graph, path):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if graph[u][v].get('blocked', False):  # Só considera se for "road" e estiver bloqueada
            return True
    return False