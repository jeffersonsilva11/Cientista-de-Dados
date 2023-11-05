import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
from sklearn.preprocessing import StandardScaler
from io import BytesIO

# URL do arquivo pickle "raw"
url = 'https://raw.githubusercontent.com/jeffersonsilva11/Cientista-de-Dados/main/modulo-38/model_final.pkl'

# Baixar o arquivo do modelo pickle
response = requests.get(url)
model = pickle.loads(response.content)

# Função para o pré-processamento dos dados
def preprocessamento(df):
    try:
        # Convertendo colunas categóricas e de data/hora para numéricas
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                df[col] = df[col].astype('category').cat.codes
            elif df[col].dtype.name == 'datetime64[ns]':
                df[col] = df[col].values.astype(np.int64) // 10 ** 9

        # Padronização dos dados
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df)
        return df_scaled
    except Exception as e:
        st.error(f"Ocorreu um erro durante o pré-processamento: {e}")
        return None

# Função para realizar a escoragem
def escoragem(df):
    # Pré-processamento dos dados
    df_processed = preprocessamento(df)
    if df_processed is not None:
        # Realizar as previsões com o modelo carregado
        predictions = model.predict(df_processed)
        return predictions
    else:
        return None

# Interface Streamlit
def main():
    st.title("Aplicação para Escoragem de Dados")

    # Carregador de arquivos FTR
    uploaded_file = st.file_uploader("Escolha um arquivo FTR para escoragem", type="ftr")
    if uploaded_file is not None:
        # Carregar o FTR para um DataFrame
        df = pd.read_feather(uploaded_file)
        
        # Mostrar o DataFrame no Streamlit (opcional)
        if st.checkbox('Mostrar dados brutos'):
            st.write(df)
        
        # Botão para realizar a escoragem
        if st.button('Escorar'):
            # Chamar a função de escoragem
            result = escoragem(df)
            if result is not None:
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
            else:
                st.error("Não foi possível realizar a escoragem devido a um erro no pré-processamento.")

# Rodar a aplicação
if __name__ == "__main__":
    main()
