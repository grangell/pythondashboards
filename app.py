import streamlit as st
from banco import obter_dataframe
#import plotly.express as px
#from utils import format_number
#from graficos import grafico_map_estado, grafico_rec_mensal, grafico_rec_estado, grafico_rec_categoria, grafico_rec_vendedores, grafico_vendas_vendedores

# filtro vendedores
#filtro_vendedor = st.sidebar.multiselect(
#    'Vendedores',
#    df['Vendedor'].unique(),
#)

#if filtro_vendedor:
#    df = df[df['Vendedor'].isin(filtro_vendedor)]

def main():
    st.title("Dashboard de Vendas :shopping_trolley:")

    st.sidebar.title('Filtro de Vendedores')

    senha_placeholder = st.empty()
    senha = senha_placeholder.text_input("Digite a senha do banco de dados:", type="password", key="senha")

    conectar_button = st.button("Conectar")

    # Adicionando uma variável de estado para rastrear o status da conexão
    conectado = False

    if conectar_button and senha:
        df = obter_dataframe(senha)  # Obter DataFrame com a senha inserida

        # Atualizar o status de conexão para True
        conectado = True

        # Exibir o DataFrame
        aba1, aba2, aba3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])
        with aba1:
            st.dataframe(df)
        #with aba2:
            #coluna1, coluna2 = st.columns(2)
        # soma preços
        #with coluna1:
            #st.metric('Receita Total', format_number(df['Preço'].sum(), 'R$'))
            #st.plotly_chart(grafico_map_estado, use_container_width=True)
            #st.plotly_chart(grafico_rec_estado, use_container_width=True)
        # qtd de linhas (vendas)
        #with coluna2:
            #st.metric('Quantidade de Vendas', format_number(df.shape[0]))
            #st.plotly_chart(grafico_rec_mensal, use_container_width=True)
            #st.plotly_chart(grafico_rec_categoria, use_container_width=True)
        #with aba3:
            #coluna1, coluna2 = st.columns(2)
        #with coluna1:
            #st.plotly_chart(grafico_rec_vendedores, use_container_width=True)
        #with coluna2:
            #st.plotly_chart(grafico_vendas_vendedores, use_container_width=True)

        # Substituir o campo de senha e o botão "Conectar" com espaços vazios
        senha_placeholder.empty()
        conectar_button = st.empty()

    # Verificar se a conexão está estabelecida para alterar o texto do botão
    if conectado:
        st.success("Conectado")
    else:
        st.warning("Aguardando conexão...")

if __name__ == "__main__":
    main()





