import pandas as pd
from sqlalchemy import create_engine

# Função para criar a conexão com o banco de dados
def criar_conexao(senha):
    server = 'TIAPRENDIZ\\SQLEXPRESS'
    database = 'Dashboards'
    username = 'sa'
    driver = 'ODBC Driver 17 for SQL Server'

    conn_str = f"mssql+pyodbc://{username}:{senha}@{server}/{database}?driver={driver}"
    
    engine = create_engine(conn_str, echo=True)  # Adicione o parâmetro echo=True para depuração

    return engine

# Função para obter o DataFrame
def obter_dataframe_conectado(engine):
    query = "SELECT * FROM Compra"
    df = pd.read_sql(query, engine, index_col='ID')
    return df