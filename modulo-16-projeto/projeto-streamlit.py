import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

sns.set(context='talk', style='ticks')

# Configuração do Streamlit
st.set_page_config(
     page_title="Análise de Renda",
     page_icon=":dollar:",
)

# Sidebar
st.sidebar.header('Navegação')
option = st.sidebar.selectbox(
    'Escolha o gráfico',
    (
        'Distribuição de Idade',
        'Distribuição de Quantidade de Pessoas por Residência',
        'Distribuição de Quantidade de Filhos',
        'Distribuição de Renda por Ano',
        # Adicione os outros gráficos aqui seguindo o mesmo formato
    )
)

# Carregando os dados
renda = pd.read_csv('./input/dados_tratados.csv')

# Função para plotar gráficos
def plot_graph(option):
    if option == 'Distribuição de Idade':
        fig, ax = plt.subplots()
        sns.histplot(renda['idade'], kde=True, ax=ax)
        ax.set_title('Distribuição de Idade')
        st.pyplot(fig)

    elif option == 'Distribuição de Quantidade de Pessoas por Residência':
        fig, ax = plt.subplots()
        sns.histplot(renda['qt_pessoas_residencia'], kde=True, ax=ax)
        ax.set_title('Distribuição de Quantidade de Pessoas por Residência')
        st.pyplot(fig)

    elif option == 'Distribuição de Quantidade de Filhos':
        fig, ax = plt.subplots()
        sns.histplot(renda['qtd_filhos'], kde=True, ax=ax)
        ax.set_title('Distribuição de Quantidade de Filhos')
        st.pyplot(fig)

    elif option == 'Distribuição de Renda por Ano':
        fig, ax = plt.subplots()
        sns.histplot(renda['ano'], kde=True, ax=ax)
        ax.set_title('Distribuição de Renda por Ano')
        st.pyplot(fig)
        
    # Adicione os outros gráficos aqui usando a mesma estrutura de if-elif

# Mostrar o gráfico
plot_graph(option)