import pandas as pd
import streamlit as st 
import time

def format_number(value, prefix = ''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'

# 1 - DataFrame Receita por Estado
# Agrupa os dados do DataFrame original com base na coluna "Local da compra" e calcula a soma dos preços para cada local de compra.
# Remove registros duplicados com base no "Local da compra" no DataFrame original e seleciona as colunas "Local da compra", "lat" e "lon".
# Mescla os dados de localização com os dados de soma de preços com base na coluna "Local da compra".
# Classifica o resultado com base na coluna "Preço" em ordem decrescente. Isso fornece uma lista de locais de compra, com informações de localização e os preços totais associados a cada local, classificados do maior para o menor preço total.
def calcular_df_rec_estado(df):
    df_rec_estado = df.groupby('Local da Compra').agg({'Preço': 'sum', 'Frete': 'first'})
    df_rec_estado = df.drop_duplicates(subset='Local da Compra')[['Local da Compra', 'Latitude', 'Longitude']].merge(df_rec_estado, left_on='Local da Compra', right_index=True).sort_values('Preço', ascending=False)
    
    df_rec_estado['Preço'] = df_rec_estado['Preço'].round(2)
    df_rec_estado['Frete'] = df_rec_estado['Frete'].round(2)

    return df_rec_estado

# 2 - DataFrame Receita Mensal
def calcular_df_rec_mensal(df):
    # Certifique-se de que 'Data da Compra' seja um DateTimeIndex
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

    df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
    df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
    df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()
    return df_rec_mensal

# 3 - DataFrame Receita por Categoria
def calcular_df_rec_categoria(df):
    df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)
    return df_rec_categoria

# DataFrame Vendedores
def calcular_df_vendedores(df):
    df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))
    return df_vendedores

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    success = st.success(
        'Arquivo baixado com sucesso',
        icon="✅"
        )
    time.sleep(3)
    success.empty()

