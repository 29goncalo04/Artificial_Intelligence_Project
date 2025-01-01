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
        vehicles_init = data['vehicles']
        grafo = create_graph(data)
        print("Dados carregados e grafo criado com sucesso.")
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
                resultado = bfs(grafo, start, goal, vehicles_init)
                for tipo, (best_path, cost) in resultado.items():
                    if best_path:
                        print(f"Veículo {tipo} | Caminho encontrado: {' -> '.join(best_path)}")
                    else:
                        print(f"Nenhum caminho encontrado para o veículo {tipo}")
            elif opcao == 3:
                print("\nProcura em Profundiade (DFS):")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                resultado = dfs(grafo, start, goal, vehicles_init)
                for tipo, (best_path, cost) in resultado.items():
                    if best_path:
                        print(f"Veículo {tipo} | Caminho encontrado: {' -> '.join(best_path)}")
                    else:
                        print(f"Nenhum caminho encontrado para o veículo {tipo}")
            elif opcao == 4:
                print("\nProcura com Custo Uniforme:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                resultado = uniform_cost_search(grafo, start, goal, vehicles_init)
                for tipo, (best_path, cost) in resultado.items():
                    if best_path:
                        print(f"Veículo {tipo} | Caminho encontrado: {' -> '.join(best_path)}")
                    else:
                        print(f"Nenhum caminho encontrado para o veículo {tipo}")
            elif opcao == 5:
                print("\nProcura Greedy:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                resultado = greedy_search(grafo, start, goal, vehicles_init)
                for tipo, (best_path, cost) in resultado.items():
                    if best_path:
                        print(f"Veículo {tipo} | Caminho encontrado: {' -> '.join(best_path)}")
                    else:
                        print(f"Nenhum caminho encontrado para o veículo {tipo}")
            elif opcao == 6:
                print("\nProcura com A*:")
                start = input("Escreva o nó inicial: ")
                goal = input("Escreva o nó final: ")
                resultado = a_star_search(grafo, start, goal, vehicles_init)
                for tipo, (best_path, cost) in resultado.items():
                    if best_path:
                        print(f"Veículo {tipo} | Caminho encontrado: {' -> '.join(best_path)}")
                    else:
                        print(f"Nenhum caminho encontrado para o veículo {tipo}")
            elif opcao == 7:
                print("\nDistribuição de mantimentos:")
                start = input("Escreva o nó inicial: ")
                results = compare_algorithms(grafo, start, vehicles_init)
                # Dicionário para armazenar os veículos que chegam a tempo para cada cidade
                vehicles_in_time_for_goal = {}

                # Iterando sobre as cidades (goals)
                for goal, algorithm_results in results.items():
                    vehicles_in_time = []

                    print(f"\nMelhores caminhos para a cidade {goal}:")

                    # Iterando sobre os veículos
                    for tipo, (best_path, best_cost) in algorithm_results.items():
                        if best_path:
                            print(f"  Veículo: {tipo} | Caminho: {' -> '.join(best_path)} | Custo: {best_cost}")
                            vehicle_in_time = calculate_vehicle_in_time(best_path, tipo, grafo, vehicles_init)
                            if vehicle_in_time:
                                for vehicle, travel_time in vehicle_in_time:
                                    vehicles_in_time.append((vehicle, travel_time))
                                    print(f"    O veículo {vehicle['type']} chega a tempo em {travel_time} minutos")
                            else:
                                    print(f"    O veículo {tipo} não chega a tempo")
                        else:
                            print(f"  Veículo: {tipo} | Nenhum caminho encontrado")
                    if vehicles_in_time:
                        vehicles_in_time_for_goal[goal] = vehicles_in_time
                        population = get_population(grafo, best_path)
                        used_vehicles= otimizar_veiculos(population, vehicles_in_time)
                        formatted_vehicles = ', '.join([f"{quantidade} x {tipo}" for tipo, quantidade in used_vehicles])
                        print(f"Veículos usados para ir para {goal}: {formatted_vehicles}")
                    else:
                        print(f"Nenhum veículo chega a tempo a {goal}")
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