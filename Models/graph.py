import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


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
            #heuristic=next((h['heuristic'] for h in data['heuristics'] if h['id'] == zone['id']), None)
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



def draw_graph(graph):
    # Desenhar o grafo com uma disposição circular dos nós
    pos = {node: graph.nodes[node]['location'] for node in graph.nodes}
    
    # Definir a cor dos nós, com Lisboa sendo amarela e os outros nós sendo azul claro
    node_colors = ['skyblue' for node in graph.nodes]

    # Desenhar o grafo com as arestas
    plt.figure(figsize=(10, 8))  # Tamanho da figura
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold', edge_color='gray', arrows=True)

    # Obter os rótulos das arestas (distâncias)
    edge_labels = nx.get_edge_attributes(graph, 'distance')

    # Desenhar os rótulos das arestas com as distâncias
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6, font_weight='bold', font_color='black')

    # Mostrar o gráfico
    plt.title("Grafo de Zonas e Conexões")
    plt.show()