import pandas as pd
from sqlalchemy import create_engine

def obter_dataframe(senha):
    server = 'TIAPRENDIZ\SQLEXPRESS'
    database = 'Dashboards'
    username = 'sa'
    driver = 'ODBC Driver 17 for SQL Server'

    conn_str = f'mssql+pyodbc://{username}:{senha}@{server}/{database}?driver={driver}'

    engine = create_engine(conn_str)

    query = "SELECT * FROM Compra"

    df = pd.read_sql(query, engine, index_col='ID')

    return df