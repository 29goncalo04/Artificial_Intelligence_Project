import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def draw_graph(graph):
    # Obter as posições dos nós
    pos = {node: graph.nodes[node]['location'] for node in graph.nodes}
    
    # Definir a cor dos nós
    node_colors = ['skyblue' for node in graph.nodes]

    # Desenhar o grafo com as arestas
    plt.figure(figsize=(10, 8))  # Tamanho da figura
    nx.draw(
        graph, pos, with_labels=True, node_size=2000, node_color=node_colors,
        font_size=10, font_weight='bold', edge_color='gray', arrows=True
    )

    # Criar os rótulos das arestas incluindo distância, status de bloqueio, clima e tipo
    edge_labels = {
        (u, v): f"{d['distance']} km\n{'Bloqueada' if d['blocked'] else ''}\n{d['weather']}\n{d['type']}"
        for u, v, d in graph.edges(data=True)
    }

    # Desenhar os rótulos das arestas
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6, font_weight='bold', font_color='black')

    # Mostrar o gráfico
    plt.title("Grafo de Zonas e Conexões")
    plt.show()