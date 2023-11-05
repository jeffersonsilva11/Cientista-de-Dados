# app.py

import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler # ou qualquer outro pré-processador necessário

# Carregando o modelo treinado (ajuste o caminho conforme necessário)
modelo = pickle.load(open('https://github.com/jeffersonsilva11/Cientista-de-Dados/blob/main/modulo-38/model_final.pkl', 'rb'))

# Função para o pré-processamento dos dados (ajuste conforme seu pré-processamento)
def preprocessamento(df):
    # Exemplo de pré-processamento: padronização dos dados
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    return df_scaled

# Função para realizar a escoragem
def escoragem(df):
    # Pré-processamento dos dados
    df_processed = preprocessamento(df)
    # Realizar as previsões com o modelo carregado
    predictions = modelo.predict(df_processed)
    return predictions

# Interface Streamlit
def main():
    st.title("Aplicação para Escoragem de Dados de Treino")

    # Carregador de arquivos CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para escoragem", type="csv")
    if uploaded_file is not None:
        # Carregar o CSV para um DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Mostrar o DataFrame no Streamlit (opcional)
        if st.checkbox('Mostrar dados brutos'):
            st.write(df)
        
        # Botão para realizar a escoragem
        if st.button('Escorar'):
            # Chamar a função de escoragem
            result = escoragem(df)
            # Adicionar as previsões ao DataFrame
            df['Previsão'] = result
            # Mostrar os resultados
            st.write("Resultados da Escoragem:")
            st.write(df)
            # Download dos resultados como CSV
            st.download_button(label='Download dos Resultados em CSV',
                               data=df.to_csv().encode('utf-8'),
                               file_name='resultados_escoragem.csv',
                               mime='text/csv')

# Rodar a aplicação
if __name__ == "__main__":
    main()
