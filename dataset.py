import json
import pandas as pd

# abrindo e carregando dados json
file = open('dados/vendas.json')
data = json.load(file)

# dataframe do pandas
df = pd.DataFrame.from_dict(data)

df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format = '%d/%m/%Y')
df['Frete'] = df['Frete'].apply(lambda x: '{:,.2f}'.format(x))
df['Preço'] = df['Preço'].astype(int)

print(df)

file.close()