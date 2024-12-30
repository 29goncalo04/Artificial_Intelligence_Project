from Utils.data_loader import*
from Utils.visualizer import*
from Models.graph import*
from Models.vehicle import*
from Algorithms.heuristics import*
from Algorithms.uninformed import*
from Algorithms.informed import*
from Algorithms.compare import*

def menu():
    # Carregar dados do ficheiro JSON
    try:
        file_path = "data.json"
        data = load_data_from_json(file_path)
        vehicles = data['vehicles']
        grafo = create_graph(data)
        print("Dados carregados e grafo criado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return

    # Loop do menu
    while True:
        print("\nMenu de Opções:")
        print("1. Visualizar o grafo")
        print("2. Procura em Largura (BFS)")
        print("3. Procura em Profundidade (DFS)")
        print("4. Procura com Custo Uniforme")
        print("5. Procura Greedy")
        print("6. Procura com A*")
        print("7. Distribuição de mantimentos")
        print("8. Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                draw_graph(grafo)
            elif opcao == 2:
                print("\nProcura em Largura (BFS):")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                path, cost = bfs(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 3:
                print("\nProcura em Profundiade (DFS):")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                path, cost = dfs(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 4:
                print("\nProcura com Custo Uniforme:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                path, cost = uniform_cost_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 5:
                print("\nProcura Greedy:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                path, cost = greedy_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 6:
                print("\nProcura com A*:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                path, cost = a_star_search(grafo, start, goal)
                if path:
                    print(f"Caminho encontrado: {' -> '.join(path)}")
                else:
                    print("Nenhum caminho encontrado.")
            elif opcao == 7:
                print("\nDistribuição de mantimentos:")
                start = input("Escreva o nó inicial: ")
                results = compare_algorithms(grafo, start)
                for goal, best_path in results.items():
                    if best_path:
                        #print(f"Melhor caminho para {goal}: {' -> '.join(best_path)}")
                        best_vehicle, best_time = calculate_fastest_vehicle(best_path, vehicles, grafo)
                        print(f"Melhor veículo para {goal}: {best_vehicle}")
                    else:
                        print(f"Não foi encontrado nenhum caminho para {goal}.")
            elif opcao == 8:
                print("A sair...")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

# Executar o menu
if __name__ == "__main__":
    menu()