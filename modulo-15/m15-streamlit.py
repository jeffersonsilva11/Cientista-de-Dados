# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np

# 1. Título e subtítulo
st.title("Aplicativo Streamlit Simples")
st.subheader("Explorando 20 recursos do Streamlit")

# 2. Adicionando um seletor de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

# 3. Ler arquivo CSV (usando caching para melhorar a performance)
@st.cache_data
def load_data():
    return pd.read_csv(uploaded_file)

if uploaded_file:
    df = load_data()

    # 4. Mostrando informações básicas usando markdown
    st.markdown("### Informações Básicas")
    st.write(f"Número de linhas: {df.shape[0]}")
    st.write(f"Número de colunas: {df.shape[1]}")

    # 5. Mostrando as primeiras linhas do dataframe
    st.dataframe(df.head())

    # 6. Checkbox para mostrar estatísticas descritivas
    if st.checkbox("Mostrar estatísticas descritivas"):
        st.write(df.describe())

    # 7. MultiSelect para escolher colunas a serem exibidas
    colunas_selecionadas = st.multiselect('Selecione as colunas para exibir:', df.columns)
    st.write(df[colunas_selecionadas].head())



    # 8. Slider para escolher número de linhas a serem exibidas
    row_num = st.slider("Escolha o número de linhas para visualizar", 1, df.shape[0])
    st.dataframe(df.head(row_num))

    # 9. Plot de um gráfico
    if st.checkbox("Mostrar gráfico"):
        st.line_chart(df[colunas_selecionadas].dropna())

    # 10. Uso do session state para manter estado entre interações
    if "contador" not in st.session_state:
        st.session_state.contador = 0

    # 11. Botão para incrementar contador
    if st.button("Clique para contar"):
        st.session_state.contador += 1

    # 12. Mostrando o valor do contador
    st.write(f"Contador: {st.session_state.contador}")

    # 13. Texto Input para personalizar título
    user_input = st.text_input("Defina um título para o app")
    if user_input:
        st.title(user_input)

    # 14. Radio button para seleção de opções
    option = st.radio("Escolha uma opção", ["A", "B", "C"])
    st.write(f"Você selecionou: {option}")

    # 15. Color picker
    color = st.color_picker("Escolha uma cor")
    st.write(f"Você selecionou a cor: {color}")

    # 16. Date input
    date = st.date_input("Escolha uma data")
    st.write(f"Você selecionou a data: {date}")

    # 17. Time input
    time = st.time_input("Escolha um horário")
    st.write(f"Você selecionou o horário: {time}")

    # 18. Number input
    num_input = st.number_input("Insira um número", min_value=0, max_value=100, value=50)
    st.write(f"Você inseriu o número: {num_input}")

    # 19. File uploader para múltiplos arquivos
    uploaded_files = st.file_uploader("Escolha arquivos", accept_multiple_files=True)
    for file in uploaded_files:
        st.write(file.name)

    # 20. Spinner para mostrar operação de carregamento
    with st.spinner("Aguarde..."):
        st.write("Operação concluída!")
