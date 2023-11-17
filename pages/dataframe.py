import streamlit as st
import os
from banco import criar_conexao, obter_dataframe_conectado
from utils import convert_csv, mensagem_sucesso
from dotenv import load_dotenv

load_dotenv()

# Verifica se o DataFrame já está na sessão
if 'df' not in st.session_state or st.session_state.df is None:
    # Se não estiver, conecta-se ao banco de dados para obter o DataFrame
    senha = os.getenv("PASSWORD_SQL")
    conexao = criar_conexao(senha)
    st.session_state.df = obter_dataframe_conectado(conexao)

# Inicializa a variável query se ainda não estiver na sessão
if 'query' not in st.session_state:
    st.session_state.query = None

st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(st.session_state.df.columns),
        list(st.session_state.df.columns)
    )
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as categorias',
        st.session_state.df['Categoria do Produto'].unique(),
        st.session_state.df['Categoria do Produto'].unique()
    )
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o Preço',
        0, 5000,
        (0, 5000)
    )
with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a data',
        (st.session_state.df['Data da Compra'].min(),
        st.session_state.df['Data da Compra'].max())
    )

# Atualiza a variável query com a nova consulta
query = '''
    `Categoria do Produto` in @categorias and \
    @preco[0] <= Preço <= @preco[1] and \
    @data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''
st.session_state.query = query

# Aplica a consulta ao DataFrame
filtro_dados = st.session_state.df.query(query)
filtro_dados = filtro_dados[colunas]
st.dataframe(filtro_dados)

st.markdown(f'A tabela possui :blue[{filtro_dados.shape[0]}] linhas e :blue [{filtro_dados.shape[1]}] colunas')
st.markdown('Escreva um nome do arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input(
        'Digite o nome do arquivo',
        label_visibility = 'collapsed',
    )
    nome_arquivo += '.csv'
with coluna2:
    st.download_button(
        'Baixar arquivo',
        data=convert_csv(filtro_dados),
        file_name=nome_arquivo,
        mime='text/csv',
        on_click=mensagem_sucesso
    )