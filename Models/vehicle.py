from Models.zone import*
from Models.graph import*

def get_vehicle_speed(vehicle):
    return vehicle['speed']


def calculate_travel_time(path, vehicle, graph):
    """
    Calcula o tempo total de viagem para um caminho específico levando em conta
    as condições meteorológicas de cada conexão.

    Args:
        path (list): Lista de cidades ou zonas que formam o caminho (ex: ['Lisboa', 'Leiria', 'Coimbra', 'Aveiro', 'Porto']).
        vehicle_speed (float): Velocidade do veículo (em km/h).
        graph (networkx.DiGraph): O grafo contendo as conexões e as condições meteorológicas associadas.

    Returns:
        float: O tempo total de viagem em minutos.
    """

    vehicle_speed = get_vehicle_speed(vehicle)

    total_travel_time = 0.0

    # Iterar sobre as conexões entre as cidades no caminho
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]

        # Verificar se a aresta existe entre as cidades
        distance = graph[start][end]['distance']
        weather = graph[start][end]['weather']
        # Definir o fator meteorológico baseado nas condições
        if weather == "sol":
            weather_factor = 1.0  # Sem impacto
        elif weather == "chuva":
            weather_factor = 0.6  # 40% de redução na velocidade
        elif weather == "neve":
            weather_factor = 0.4  # 60% de redução na velocidade
        elif weather == "vento":
            weather_factor = 0.9  # 10% de redução na velocidade
        # Calcular a velocidade ajustada com o fator meteorológico
        adjusted_speed = vehicle_speed * weather_factor
        if adjusted_speed <= 0:
            raise ValueError(f"Velocidade ajustada inválida para a conexão {start} -> {end}: {adjusted_speed} km/h")
        # Calcular o tempo de viagem para essa conexão
        travel_time = distance / adjusted_speed
        total_travel_time += travel_time

    total_travel_time *= 60
    return total_travel_time


def calculate_fastest_vehicles(path, vehicles, graph):
    critical_time = get_critical_time(graph, path)
    in_time = []
    out_of_time = []

    # Iterar sobre os veículos para calcular o tempo de viagem
    for vehicle in vehicles:
        # Calcular o tempo de viagem para o veículo atual
        total_travel_time = calculate_travel_time(path, vehicle, graph)
        total_travel_time = round(total_travel_time)

        # Verificar se o veículo chega a tempo
        if total_travel_time <= critical_time:
            in_time.append((vehicle, total_travel_time))
        else:
            out_of_time.append((vehicle, total_travel_time))

    # Ordenar as listas pela capacidade em ordem decrescente
    in_time.sort(key=lambda x: x[0]['capacity'], reverse=True)
    out_of_time.sort(key=lambda x: x[0]['capacity'], reverse=True)

    return in_time, out_of_time


def enough_fuel(distance, vehicles):
    best_vehicles = []
    for vehicle in vehicles:
        if vehicle['range'] >= distance:
            best_vehicles.append(vehicle)  # Adiciona o tipo do veículo à lista
    return best_vehicles


# def generate_route_with_refueling(total_distance, vehicles):
#     results = []

#     for vehicle in vehicles:
#         remaining_distance = total_distance
#         remaining_range = vehicle['range']
#         route_with_refueling = []

#         while remaining_distance > 0:
#             if remaining_distance > remaining_range:
#                 # Adiciona um reabastecimento e percorre o máximo permitido pelo veículo.
#                 route_with_refueling.append(f"Travel {remaining_range} km")
#                 route_with_refueling.append("Refuel")
#                 remaining_distance -= remaining_range
#                 remaining_range = vehicle['range']  # Reabastece.
#             else:
#                 # Último trecho da rota, veículo alcança o destino.
#                 route_with_refueling.append(f"Travel {remaining_distance} km")
#                 remaining_distance = 0  # Viagem concluída.

#         results.append({
#             "vehicle": vehicle['type'],
#             "route_with_refueling": route_with_refueling
#         })

#     return results    




def discard_vehicles_for_road(graph, path, vehicles):
    if(has_air_connection(graph, path)):
        vehicles = [vehicle for vehicle in vehicles if vehicle.get('type') != 'camião']
    return vehicles

def discard_vehicles_for_water(graph, path, vehicles):
    if(has_road_connection(graph, path)):
        vehicles = [vehicle for vehicle in vehicles if vehicle.get('type') != 'navio']
    return vehicles






def otimizar_veiculos(populacao, veiculos_rapidos, veiculos_lentos):
    total_capacidade = 0
    veiculos_utilizados = []
    menor_tempo = float('inf')
    # Tenta usar veículos rápidos (que chegam a tempo)
    for veiculo, tempo in veiculos_rapidos:
        while total_capacidade + veiculo['capacity'] <= populacao:
            total_capacidade += veiculo['capacity']
            veiculos_utilizados.append(veiculo['type'])
            if tempo < menor_tempo:
                menor_tempo = tempo
            if total_capacidade == populacao:
                return veiculos_utilizados, menor_tempo
    # Tenta usar veículos que não chegam a tempo
    for veiculo, tempo in veiculos_lentos:
        while total_capacidade + veiculo['capacity'] <= populacao:
            total_capacidade += veiculo['capacity']
            veiculos_utilizados.append(veiculo['type'])
            if tempo < menor_tempo:
                menor_tempo = tempo
            if total_capacidade == populacao:
                return veiculos_utilizados, menor_tempo
    melhor_veiculo = None
    menor_excedente = float('inf')
    # Percorre todas as opções de veículos novamente
    for veiculo, tempo in veiculos_rapidos + veiculos_lentos:
        excedente = total_capacidade + veiculo['capacity'] - populacao
        # Verifica se o veículo pode ser usado sem exceder a população
        if 0 <= excedente < menor_excedente:
            melhor_veiculo = veiculo
            menor_excedente = excedente
            menor_tempo = tempo
    # Adiciona o veículo que causou o menor excedente
    if melhor_veiculo:
        total_capacidade += melhor_veiculo['capacity']
        veiculos_utilizados.append(melhor_veiculo['type'])
    return veiculos_utilizados, menor_tempo












# def distribuir_recursos_veiculos_limitados(zones, vehicles, graph):
#     """
#     Distribui os recursos para maximizar a cobertura das zonas afetadas com um número limitado de veículos.
    
#     Args:
#         zones (list): Lista de zonas afetadas com informações sobre prioridade, população e tempo crítico.
#         vehicles (list): Lista de veículos disponíveis com capacidade, velocidade, alcance e tipo.
#         graph (networkx.DiGraph): Grafo representando as conexões entre as zonas e condições meteorológicas.
    
#     Returns:
#         dict: Um dicionário com as zonas atendidas, os veículos utilizados e a cobertura total.
#     """
#     # Ordenar zonas por prioridade (decrescente) e população (decrescente)
#     zones = sorted(zones, key=lambda z: (-z['priority'], -z['population']))
    
#     cobertura_total = 0
#     zonas_atendidas = []
#     veiculos_usados = []

#     for zone in zones:
#         path = encontrar_melhor_caminho(zone['id'], graph)  # Função para encontrar o melhor caminho
#         critical_time = zone['critical_time']
#         populacao_afetada = zone['population']
        
#         # Filtrar veículos com combustível suficiente
#         distance = calcular_distancia_total(path, graph)
#         veiculos_filtrados = enough_fuel(distance, vehicles)

#         # Separar veículos que chegam a tempo
#         veiculos_rapidos, veiculos_lentos = calculate_fastest_vehicles(path, veiculos_filtrados, graph)

#         # Otimizar veículos para atender a população da zona
#         veiculos_selecionados, capacidade_coberta = otimizar_veiculos(populacao_afetada, veiculos_rapidos, veiculos_lentos)

#         # Se veículos foram encontrados para atender à zona
#         if capacidade_coberta > 0:
#             cobertura_total += capacidade_coberta
#             zonas_atendidas.append({
#                 'zone_id': zone['id'],
#                 'vehicles': veiculos_selecionados,
#                 'covered_population': capacidade_coberta
#             })
#             # Remover veículos usados da lista disponível
#             for veiculo_tipo in veiculos_selecionados:
#                 for vehicle in vehicles:
#                     if vehicle['type'] == veiculo_tipo:
#                         vehicles.remove(vehicle)
#                         veiculos_usados.append(vehicle)
#                         break
    
#     return {
#         'total_coverage': cobertura_total,
#         'zones_attended': zonas_atendidas,
#         'vehicles_used': veiculos_usados
#     }