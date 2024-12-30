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
        float: O tempo total de viagem em horas.
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

    return total_travel_time


def calculate_fastest_vehicle(path, vehicles, graph):
    fastest_vehicle = None
    fastest_time = float('inf')  # Inicia com tempo infinito

    # Iterar sobre os veículos para calcular o tempo de viagem
    for vehicle in vehicles:
        # Calcular o tempo de viagem para o veículo atual
        total_travel_time = calculate_travel_time(path, vehicle, graph)
        
        # Verificar se o veículo atual é o mais rápido
        if total_travel_time < fastest_time:
            fastest_vehicle = vehicle['type']
            fastest_time = total_travel_time

    return fastest_vehicle, fastest_time