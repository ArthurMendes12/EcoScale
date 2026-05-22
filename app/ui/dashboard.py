# app/ui/dashboard.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def renderizar_metricas(indicadores: dict):
    """
    Recebe um dicionário de indicadores e cria colunas no Streamlit para exibi-los.
    """
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total de Processos", indicadores["Total de Processos (Nós)"])
    col2.metric("Total de Fluxos", indicadores["Total de Fluxos (Arestas)"])
    col3.metric("Emergia Circulante", f"{indicadores['Emergia Total Circulante']:.2f}")

def plotar_rede(grafo: nx.DiGraph):
    """
    Gera uma visualização visual do grafo usando Matplotlib e injeta no Streamlit.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define o layout (posição dos nós na tela)
    pos = nx.spring_layout(grafo, seed=42)
    
    # Desenha os nós e rótulos
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=10, font_weight='bold', ax=ax, arrows=True)
    
    # Desenha os valores dos fluxos nas setas
    labels_arestas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels_arestas, ax=ax)
    
    # Exibe no Streamlit
    st.pyplot(fig)