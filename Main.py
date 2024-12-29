from Utils.data_loader import*
from Utils.visualizer import*
from Models.graph import*
from Algorithms.heuristics import*
from Algorithms.uninformed import*
from Algorithms.informed import*

def menu():
    # Carregar dados do ficheiro JSON
    try:
        file_path = "data.json"
        data = load_data_from_json(file_path)
        grafo = create_graph(data)
        print("Dados carregados e grafo criado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return

    # Loop do menu
    while True:
        print("\nMenu de Opções:")
        print("1. Visualizar o grafo")
        print("2. Busca em Largura (BFS)")
        print("3. Busca em Profundidade (DFS)")
        print("4. Busca com Custo Uniforme")
        print("5. Busca com Greedy")
        print("6. Busca com A*")
        print("7. Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                draw_graph(grafo)
            # elif opcao == 3:
            #     # Exibir as heurísticas calculadas
            #     nodo_final = str(input("Nodo final:"))
            #     calculate_heuristics(grafo, nodo_final)
            #     #for node_id in grafo.nodes:
            #     #    print(f"{node_id}: {grafo.nodes[node_id]['heuristic']:.2f}")
            elif opcao == 2:
                print("\nBusca em Largura (BFS):")
                start = input("Digite o nó inicial: ")
                goal = input("Digite o nó final: ")
                path = bfs(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 3:
                print("\nBusca em Profundiade (DFS):")
                start = input("Digite o nó inicial: ")
                goal = input("Digite o nó final: ")
                path = dfs(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 4:
                print("\nBusca com Custo Uniforme:")
                start = input("Digite o nó inicial: ")
                goal = input("Digite o nó final: ")
                path = uniform_cost_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 5:
                print("\nBusca com Greedy:")
                start = input("Digite o nó inicial: ")
                goal = input("Digite o nó final: ")
                path = greedy_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 6:
                print("\nBusca com A*:")
                start = input("Digite o nó inicial: ")
                goal = input("Digite o nó final: ")
                path = a_star_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 7:
                print("A sair...")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

# Executar o menu
if __name__ == "__main__":
    menu()