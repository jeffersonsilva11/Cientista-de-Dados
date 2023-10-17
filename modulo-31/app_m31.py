import pandas as pd
import streamlit as st
import base64

# Função para o upload do arquivo
def user_upload():
    uploaded_file = st.file_uploader("Selecione a base de dados (.csv)", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, infer_datetime_format=True, parse_dates=['DiaCompra'])
        return data
    return None

def recencia_class(x, param, quartis):
    if x <= quartis[param][0.25]:
        return 1
    elif x <= quartis[param][0.50]:
        return 2
    elif x <= quartis[param][0.75]:
        return 3
    else:
        return 4

def freq_val_class(x, param, quartis):
    if x <= quartis[param][0.25]:
        return 4
    elif x <= quartis[param][0.50]:
        return 3
    elif x <= quartis[param][0.75]:
        return 2
    else:
        return 1

# Função para criar o link de download
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_excel(index=True, engine='openpyxl')

    b64 = base64.b64encode(object_to_download).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# Título da página
st.title('Aplicação de Clusterização RFV')

df_compras = user_upload()

if df_compras is not None:
    st.write("Base carregada com sucesso!")

    # Realizando as opções para criar o RFV
    dia_atual = df_compras['DiaCompra'].max()
    df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
    df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
    df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
    df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

    df_frequencia = df_compras[['ID_cliente', 'CodigoCompra']].groupby('ID_cliente').count().reset_index()
    df_frequencia.columns = ['ID_cliente', 'Frequencia']

    df_valor = df_compras[['ID_cliente', 'ValorTotal']].groupby('ID_cliente').sum().reset_index()
    df_valor.columns = ['ID_cliente', 'Valor']

    # Criando a clusterização RFV
    df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
    df_RFV = df_RF.merge(df_valor, on='ID_cliente')
    df_RFV.set_index('ID_cliente', inplace=True)

    quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])

    df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
    df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
    df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))

    df_RFV['RFV_Score'] = df_RFV.R_quartil.map(str) + df_RFV.F_quartil.map(str) + df_RFV.V_quartil.map(str)

    # Mostrando o resultado para o usuário
    st.write(df_RFV)

    # Permitindo que o usuário baixe o resultado
    tmp_download_link = download_link(df_RFV, 'RFV_output.xlsx', 'Clique aqui para baixar o arquivo excel!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)
