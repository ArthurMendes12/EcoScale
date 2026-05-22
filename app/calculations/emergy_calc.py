# app/calculations/emergy_calc.py
import networkx as nx
import numpy as np

def calcular_emergia_entrada(grafo: nx.DiGraph, no_destino: str) -> float:
    """
    Calcula a soma de todos os fluxos que entram em um nó específico.
    Utilizamos álgebra básica com listas que poderiam ser convertidas em arrays NumPy.
    """
    # Se o nó não existir no grafo, retorna 0
    if no_destino not in grafo:
        return 0.0
        
    # Busca todas as arestas que entram no 'no_destino'
    arestas_entrada = grafo.in_edges(no_destino, data=True)
    
    # Extrai apenas os valores (pesos) dessas conexões
    valores = [dados['weight'] for origem, destino, dados in arestas_entrada]
    
    # Usa NumPy para somar os valores (álgebra simplificada)
    soma_total = np.sum(valores)
    
    return float(soma_total)

def calcular_indicadores_gerais(grafo: nx.DiGraph) -> dict:
    """
    Calcula indicadores básicos de toda a rede LCI.
    """
    todos_pesos = [dados['weight'] for u, v, dados in grafo.edges(data=True)]

    return {
        "Total de Processos (Nós)": len(grafo.nodes),
        "Total de Fluxos (Arestas)": len(grafo.edges),
        "Emergia Total Circulante": np.sum(todos_pesos)
    }