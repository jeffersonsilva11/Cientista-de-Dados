import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_graphs(df, diretorio):
    # Média da idade da mãe por mês
    plt.figure(figsize=(10, 6))
    plt.bar(df['DTNASC'].dt.strftime('%Y-%m-%d'), df['IDADEMAE'])
    plt.title('Média da Idade da Mãe por Mês')
    plt.xlabel('Data')
    plt.ylabel('Idade da Mãe')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(diretorio, 'media_idade_mae.png'))
    plt.close()
    
    # Média do peso do bebê por mês
    plt.figure(figsize=(10, 6))
    plt.bar(df['DTNASC'].dt.strftime('%Y-%m-%d'), df['PESO'])
    plt.title('Média do Peso do Bebê por Mês')
    plt.xlabel('Data')
    plt.ylabel('Peso (g)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(diretorio, 'media_peso_bebe.png'))
    plt.close()
    
    # Média do APGAR1 por mês
    plt.figure(figsize=(10, 6))
    plt.bar(df['DTNASC'].dt.strftime('%Y-%m-%d'), df['APGAR1'])
    plt.title('Média do APGAR1 por Mês')
    plt.xlabel('Data')
    plt.ylabel('APGAR1')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(diretorio, 'media_apgar1.png'))
    plt.close()

def verificar_arquivo(mes):
    filename = f'sinasc_{mes}.csv'
    return os.path.exists(filename)

def criar_diretorio(ano, mes):
    dirname = f'{ano}-{mes}'
    os.makedirs(dirname, exist_ok=True)
    return dirname

# Mapear abreviaturas para números
mapa_meses = {
    "MAR": "03", 
    "ABR": "04", 
    "MAI": "05",
    "JUN": "06",
    "JUL": "07",
    "AGO": "08",
    "SET": "09",
    "OUT": "10",
    "NOV": "11",
    "DEZ": "12"
}

# Pegar abreviaturas da linha de comando
meses_input = sys.argv[1:]

# Definir ano, neste exemplo estamos usando 2019, mas você pode adaptar
ano = "2019"

for mes_abrev in meses_input:
    mes_num = mapa_meses.get(mes_abrev.upper())
    
    if not mes_num:
        print(f"Abreviatura {mes_abrev} não reconhecida.")
        continue
    
    if verificar_arquivo(mes_abrev):
        dirname = criar_diretorio(ano, mes_num)
        df = pd.read_csv(f'sinasc_{mes_abrev}.csv', parse_dates=['DTNASC'])
        plot_graphs(df, dirname)  
    else:
        print(f"Arquivo para {mes_abrev} não encontrado.")