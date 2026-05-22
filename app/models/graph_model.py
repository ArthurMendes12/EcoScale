import networkx as nx
import pandas as pd

def build_graph(df: pd.DataFrame) -> nx.DiGraph:
    """
    Transforma um DataFrame do Pandas em um Grafo Direcionado.
    """
    G = nx.DiGraph()
    
    for index, row in df.iterrows():
        G.add_edge(row['origem'], row['destino'], weight=row['valor'])
        
    return G