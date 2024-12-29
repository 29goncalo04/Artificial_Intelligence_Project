import networkx as nx
import random

def generate_weather_conditions():
    """
    Gera uma condição meteorológica aleatória.
    """
    weather_conditions = ["sol", "chuva", "neve", "vento"]
    return random.choice(weather_conditions)

def create_graph(data):
    graph = nx.DiGraph()  # Grafo direcionado

    # Adicionar os nós com atributos
    for zone in data['zones']:
        graph.add_node(
            zone['id'],
            priority=zone['priority'],
            population=zone['population'],
            critical_time=zone['critical_time'],
            location=tuple(zone['location']),  # Converter a lista para tupla
            weather=generate_weather_conditions()
        )

    # Adicionar as arestas com atributos
    for connection in data['connections']:
        graph.add_edge(
            connection['from'],
            connection['to'],
            distance=connection['distance'],
            type=connection['type'],
            blocked=connection['blocked']
        )
        # Adicionar a aresta reversa automaticamente
        graph.add_edge(
            connection['to'],
            connection['from'],
            distance=connection['distance'],
            type=connection['type'],
            blocked=connection['blocked']
        )
    return graph