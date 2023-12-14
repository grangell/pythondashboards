import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Definição da classe Compra
class Compra(Base):
    __tablename__ = 'Compra'
    __table_args__ = {'quote': '`'}  # Isso permite que o SQLAlchemy use aspas duplas

    id = Column(Integer, primary_key=True)
    Produto = Column(String)
    Categoria_do_Produto = Column('Categoria do Produto', String) 
    Preço = Column(Float)
    Frete = Column(Float)
    Data_da_Compra = Column('Data da Compra', Date) 
    Vendedor = Column(String)
    Local_da_Compra = Column('Local da Compra', String) 
    Avaliaçao_da_Compra = Column('Avaliaçao da Compra', String) 
    Tipo_de_Pagamento = Column('Tipo de Pagamento', String) 
    Quantidade_de_Parcelas = Column('Quantidade de Parcelas', Integer) 
    Latitude = Column(Float)
    Longitude = Column(Float)

# Função para criar a conexão com o banco de dados
def criar_conexao(senha):
        server = 'TIAPRENDIZ\SQLEXPRESS'
        database = 'Dashboards'
        username = 'sa'
        driver = 'ODBC Driver 17 for SQL Server'

        # Cria uma instância do SQLAlchemy Engine
        conn_str = f"mssql+pyodbc://{username}:{senha}@{server}/{database}?driver={driver}"
        engine = create_engine(conn_str, echo=True)

        # Conecta ao banco de dados
        conexao = engine.connect()

        # Armazena a conexão na sessão
        st.session_state.conexao = conexao

        return conexao

# Função para obter o DataFrame
def obter_dataframe_conectado(engine):
    query = "SELECT * FROM Compra"
    df = pd.read_sql(query, engine, index_col='ID')
    return df