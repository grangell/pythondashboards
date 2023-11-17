import streamlit as st
from banco import criar_conexao, obter_dataframe_conectado
from graficos import criar_grafico_map_estado, criar_grafico_rec_estado, criar_grafico_rec_mensal, criar_grafico_rec_categoria, criar_grafico_rec_vendedores, criar_grafico_vendas_vendedores
from utils import format_number, calcular_df_rec_estado, calcular_df_rec_mensal, calcular_df_rec_categoria, calcular_df_vendedores, convert_csv, mensagem_sucesso
from sqlalchemy.exc import OperationalError

# Função principal do aplicativo
def main():
    st.title("Dashboard de Vendas :shopping_trolley:")

    st.sidebar.title('Filtro de Vendedores')

    # Verifica se a conexão já foi estabelecida na sessão
    if 'conexao' not in st.session_state:
        st.session_state.conexao = None

    # Verifica se o DataFrame já foi carregado na sessão
    if 'df' not in st.session_state:
        st.session_state.df = None

    # Verifica se a senha já foi digitada
    if 'senha' not in st.session_state:
        st.session_state.senha = None

    # Adiciona uma variável de controle para verificar se a conexão foi bem-sucedida
    if 'conectado' not in st.session_state:
        st.session_state.conectado = False

    # Se a senha ainda não foi armazenada na sessão, solicita a senha
    if st.session_state.senha is None or not st.session_state.conectado:
        senha = st.text_input("Digite a senha do banco de dados:", type="password")
        conectar_button = st.button("Conectar")

        # Verifica se o botão foi pressionado e se a senha foi inserida
        if conectar_button and senha:
            try:
                # Tenta criar a conexão
                conexao = criar_conexao(senha)

                # Verifica se a conexão foi bem-sucedida usando uma consulta simples
                if conexao is not None:
                    try:
                        # Tenta obter o DataFrame com a conexão estabelecida
                        st.session_state.df = obter_dataframe_conectado(conexao)
                        st.session_state.senha = senha  # Armazena a senha na sessão
                        st.session_state.conectado = True  # Define como conectado
                    except OperationalError as e:
                        mensagem_erro = str(e).strip()
                        if mensagem_erro:
                            st.warning(f"Erro ao conectar: {mensagem_erro}")
                        else:
                            st.warning("Erro ao conectar.")
                        st.session_state.conectado = False        
            except Exception as e:
                st.warning(f"Senha incorreta. Por favor, tente novamente.")

    # Verifica se a conexão foi estabelecida com sucesso antes de exibir o DataFrame
    if st.session_state.conectado:
        
        df_rec_estado = calcular_df_rec_estado(st.session_state.df)
        df_rec_mensal = calcular_df_rec_mensal(st.session_state.df)
        df_rec_categoria = calcular_df_rec_categoria(st.session_state.df)
        df_vendedores = calcular_df_vendedores(st.session_state.df)
        
        # Se a senha já foi armazenada e a conexão foi estabelecida, apenas exibe o DataFrame
        aba1, aba2, aba3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])
        with aba1:
            st.dataframe(st.session_state.df)
        with aba2:
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.metric('Receita Total', format_number(st.session_state.df['Preço'].sum(), 'R$'))
                st.plotly_chart(criar_grafico_map_estado(df_rec_estado), use_container_width=True)
                st.plotly_chart(criar_grafico_rec_estado(df_rec_estado), use_container_width=True)
            with coluna2:
                st.metric('Quantidade de Vendas', format_number(st.session_state.df.shape[0]))
                st.plotly_chart(criar_grafico_rec_mensal(df_rec_mensal), use_container_width=True)
                st.plotly_chart(criar_grafico_rec_categoria(df_rec_categoria), use_container_width=True)
            with aba3:
                coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.plotly_chart(criar_grafico_rec_vendedores(df_vendedores), use_container_width=True)
            with coluna2:
                st.plotly_chart(criar_grafico_vendas_vendedores(df_vendedores), use_container_width=True)

# Executa a função principal quando o script é executado diretamente
if __name__ == "__main__":
    main()
