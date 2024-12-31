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
                for goal, (best_path, best_cost) in results.items():
                    if best_path:
                        vehicles = discard_vehicles_for_road(grafo, best_path, vehicles_init)
                        vehicles = discard_vehicles_for_water(grafo, best_path, vehicles)
                        vehicles = discard_vehicles_for_blocked_road(grafo, best_path, vehicles)
                        #vehicle_types = [veiculo['type'] for veiculo in vehicles]  
                        #print(f"\n\n\nDistância até {goal}: {best_cost}km")
                        print(f"\n\n\nMelhor caminho para {goal}: {' -> '.join(best_path)}")
                        #print(f"Veículos que fazem o trajeto: {', '.join(vehicle_types)}")                    

                        best_vehicles = enough_fuel(best_cost, vehicles)    #verifica quais têm combustivel suficiente
                        #vehicle_types = [veiculo['type'] for veiculo in best_vehicles]
                        #print(f"Veículos com combustível para {goal}: {', '.join(vehicle_types)}")

                        vehicles_in_time, vehicles_out_of_time = calculate_fastest_vehicles(best_path, best_vehicles, grafo)    #retorna quais chegam a tempo e os que não
                        #print("Veículos que chegaram a tempo:")
                        #for vehicle, travel_time in vehicles_in_time:
                        #    print(f"Veículo: {vehicle['type']}, Tempo de viagem: {travel_time} unidades de tempo")

                        # Imprimir os veículos que não chegaram a tempo
                        #print("\nVeículos que não chegaram a tempo:")
                        #for vehicle, travel_time in vehicles_out_of_time:
                        #    print(f"Veículo: {vehicle['type']}, Tempo de viagem: {travel_time} unidades de tempo")
                        population = get_population(grafo, best_path)
                        used_vehicles, best_time = otimizar_veiculos(population, vehicles_in_time, vehicles_out_of_time)
                        critical_time = get_critical_time(grafo, best_path)
                        print(f"O tempo cŕitico para chegar à região {goal} era {critical_time} min e os meios começaram a chegar após {best_time} minutos")
                        print(f"Veículos usados para ir para {goal}: {used_vehicles}")
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