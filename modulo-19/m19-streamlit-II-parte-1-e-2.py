import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

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

show_data = st.sidebar.checkbox('Mostrar Dados')  # Caixa de seleção

# Upload de arquivo
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type=["csv"])
if uploaded_file:
    renda = pd.read_csv(uploaded_file)
else:
    renda = pd.read_csv('./input/dados_tratados.csv')

# Filtro
st.sidebar.header('Filtro')
selected_ano = st.sidebar.slider('Selecione o Ano', int(renda['ano'].min()), int(renda['ano'].max()))
filtered_data = renda[renda['ano'] == selected_ano]

# Botão de download do filtro
st.download_button(
    label="Download Dados Filtrados",
    data=filtered_data.to_csv(index=False).encode('utf-8'),
    file_name=f'dados_filtrados_{selected_ano}.csv',
    mime='text/csv',
)

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

        # Retorna o gráfico para permitir o download da imagem
        return fig
        
    # Adicione os outros gráficos aqui usando a mesma estrutura de if-elif

# Mostrar o gráfico
fig = plot_graph(option)

# Mostrar os dados se a caixa de seleção estiver marcada
if show_data:
    st.dataframe(renda)

# Botões de download
csv_download = st.download_button(
    label="Download CSV",
    data=renda.to_csv(index=False).encode('utf-8'),
    file_name='dados_tratados.csv',
    mime='text/csv',
)

if fig:  # Certificar-se de que temos uma figura para baixar
    png_download = st.download_button(
        label="Download Imagem",
        data=fig.savefig("output.png", format='png').encode('utf-8'),
        file_name='grafico.png',
        mime='image/png',
    )
