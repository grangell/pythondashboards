from dataset import df
import pandas as pd
import streamlit as st
import time

#func format number
def format_number(value, prefix = ''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'

# 1 - DataFrame Receita por Estado
# Agrupa os dados do DataFrame original com base na coluna "Local da compra" e calcula a soma dos preços para cada local de compra.
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()

# Remove registros duplicados com base no "Local da compra" no DataFrame original e seleciona as colunas "Local da compra", "lat" e "lon".
# Mescla os dados de localização com os dados de soma de preços com base na coluna "Local da compra".
# Classifica o resultado com base na coluna "Preço" em ordem decrescente. Isso fornece uma lista de locais de compra, com informações de localização e os preços totais associados a cada local, classificados do maior para o menor preço total.
df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(df_rec_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

# 2 - DataFrame Receita Mensal00
df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()

# 3 - DataFrame Receita por Categoria
df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)
#print(df_rec_categoria.head())

# DataFrame Vendedores
df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

# Função para converter arquivo csv
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

