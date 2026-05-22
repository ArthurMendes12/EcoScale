# main.py
import streamlit as st
import pandas as pd
from app.models.graph_model import build_graph
from app.calculations.emergy_calc import calcular_indicadores_gerais, calcular_emergia_entrada
from app.ui.dashboard import renderizar_metricas, plotar_rede

# Configuração da página Streamlit
st.set_page_config(page_title="EcoScale - LCI Analysis", layout="wide")

st.title("🌱 EcoScale - Sistema de Análise Ambiental")
st.write("Importe seu arquivo CSV de Inventário do Ciclo de Vida (LCI) para visualizar e calcular indicadores baseados em álgebra emergética.")

# RF01: Módulo de Upload (Drag-and-drop)
arquivo_upload = st.file_uploader("Arraste e solte seu CSV aqui", type=["csv"])

if arquivo_upload is not None:
    try:
        # RF02: Leitura usando Pandas
        # RF02: Leitura usando Pandas indicando que o separador é o ponto e vírgula
        df = pd.read_csv(arquivo_upload, sep=';')
        
        # Padroniza os nomes das colunas para letras minúsculas para evitar erros
        df.columns = df.columns.str.lower()
        
        st.subheader("📋 Dados Importados")
        st.dataframe(df, use_container_width=True)
        
        # Constrói a estrutura de rede (Grafo)
        grafo = build_graph(df)
        
        # RF03: Cálculos de Emergia
        indicadores = calcular_indicadores_gerais(grafo)
        
        st.markdown("---")
        st.subheader("📊 Dashboard de Indicadores")
        
        # RF04: Dashboard de exibição
        renderizar_metricas(indicadores)
        
        col_grafico, col_analise = st.columns([2, 1])
        
        with col_grafico:
            st.subheader("🕸️ Rede de Processos LCI")
            # RF05 e RF06: Visualização da rede e Gráficos
            plotar_rede(grafo)
            
        with col_analise:
            st.subheader("🔍 Análise de Nó Específico")
            st.write("Calcule a entrada total de emergia de um processo:")
            # Permite ao usuário escolher um processo para calcular a emergia
            lista_nos = list(grafo.nodes)
            no_selecionado = st.selectbox("Selecione o processo (Nó):", lista_nos)
            
            if no_selecionado:
                resultado_no = calcular_emergia_entrada(grafo, no_selecionado)
                st.info(f"A emergia total de entrada para **{no_selecionado}** é: **{resultado_no:.2f}**")
        
        # RF07: Exportação de resultados
        st.markdown("---")
        st.subheader("💾 Exportar Resultados")
        
        # Prepara os dados calculados para download
        df_resultados = pd.DataFrame([indicadores])
        csv_saida = df_resultados.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Baixar Relatório de Indicadores (CSV)",
            data=csv_saida,
            file_name='ecoscale_relatorio.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Verifique se ele contém as colunas: poregim, destino, valor. Detalhes: {e}")
else:
    st.info("Aguardando upload do arquivo CSV para iniciar o processamento.")