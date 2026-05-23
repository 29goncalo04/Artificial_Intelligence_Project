from Models.graph import*
import json

def load_data_from_json(file_path):
    # Abrir o arquivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Retornar todos os dados carregados diretamente como um único dicionário
    return {
        'zones': data['zones'],
        'connections': data['connections'],
        'vehicles': data['vehicles']
    }