# Importação das bibliotecas necessáras
import pandas as pd
import streamlit as st

# Função para o upload do arquivo
def user_upload():
    uploaded_file = st.file_uploader("Selecione a base de dados (.csv)", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

df_compras = user_upload()

if df_compras is not None:
    st.write("Base carregada com sucesso!")

# Realizando as opções para criar o RFV
dia_atual = df_compras['DiaCompra'].max()
df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
df_recencia.columns = ['ID_cliente','DiaUltimaCompra']
df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

df_frequencia = df_compras[['ID_cliente','CodigoCompra']].groupby('ID_cliente').count().reset_index()
df_frequencia.columns = ['ID_cliente','Frequencia']

df_valor = df_compras[['ID_cliente','ValorTotal']].groupby('ID_cliente').sum().reset_index()
df_valor.columns = ['ID_cliente','Valor']

# Criando a clusterização RFV
df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
df_RFV = df_RF.merge(df_valor, on='ID_cliente')
df_RFV.set_index('ID_cliente', inplace=True)

quartis = df_RFV.quantile(q=[0.25,0.5,0.75])

# Criando os segmentos com base nos quartis
df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))

df_RFV['RFV_Score'] = df_RFV.R_quartil + df_RFV.F_quartil + df_RFV.V_quartil

# Exportando o resultado para excel
df_RFV.to_excel('RFV_output.xlsx')