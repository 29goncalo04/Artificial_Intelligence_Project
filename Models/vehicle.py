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


def calculate_vehicle_in_time(path, tipo, graph, vehicles):
    # Obtenha o tempo crítico para o caminho (goal)
    critical_time = get_critical_time(graph, path)
    vehicles_in_time = []

    # Iterar sobre os veículos para calcular o tempo de viagem
    for vehicle in vehicles:
        if vehicle['type'] == tipo:  # Filtra os veículos de acordo com o tipo
            # Calcular o tempo de viagem para o veículo atual
            total_travel_time = calculate_travel_time(path, vehicle, graph)
            total_travel_time = round(total_travel_time)

            # Verificar se o veículo chega a tempo
            if total_travel_time <= critical_time:
                vehicles_in_time.append((vehicle, total_travel_time))

    # Ordenar os veículos pela capacidade em ordem decrescente
    vehicles_in_time.sort(key=lambda x: x[0]['capacity'], reverse=True)

    return vehicles_in_time 





def otimizar_veiculos(populacao, veiculos_rapidos):
    # Ordenar os veículos por capacidade em ordem decrescente
    veiculos_rapidos = sorted(veiculos_rapidos, key=lambda x: x[0]['capacity'], reverse=True)
    total_capacidade = 0
    veiculos_utilizados = {}
    # Tenta usar veículos rápidos (que chegam a tempo)
    for veiculo, _ in veiculos_rapidos:
        while total_capacidade + veiculo['capacity'] <= populacao:
            total_capacidade += veiculo['capacity']
            veiculos_utilizados[veiculo['type']] = veiculos_utilizados.get(veiculo['type'], 0) + 1
            if total_capacidade == populacao:
                return [(tipo, quantidade) for tipo, quantidade in veiculos_utilizados.items()]
    melhor_veiculo = None
    menor_excedente = float('inf')
    # Percorre todas as opções de veículos novamente
    for veiculo, _ in veiculos_rapidos:
        excedente = total_capacidade + veiculo['capacity'] - populacao
        # Verifica se o veículo pode ser usado sem exceder a população
        if 0 <= excedente < menor_excedente:
            melhor_veiculo = veiculo
            menor_excedente = excedente
    # Adiciona o veículo que causou o menor excedente
    if melhor_veiculo:
        total_capacidade += melhor_veiculo['capacity']
        veiculos_utilizados[melhor_veiculo['type']] = veiculos_utilizados.get(melhor_veiculo['type'], 0) + 1
    return [(tipo, quantidade) for tipo, quantidade in veiculos_utilizados.items()]