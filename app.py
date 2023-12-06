import streamlit as st
from banco import criar_conexao, obter_dataframe_conectado
from sqlalchemy.sql import insert
from banco import Compra
from graficos import criar_grafico_map_estado, criar_grafico_rec_estado, criar_grafico_rec_mensal, criar_grafico_rec_categoria, criar_grafico_rec_vendedores, criar_grafico_vendas_vendedores
from utils import format_number, calcular_df_rec_estado, calcular_df_rec_mensal, calcular_df_rec_categoria, calcular_df_vendedores
from sqlalchemy.exc import OperationalError

def main():
    
    st.title("Dashboard de Vendas :shopping_trolley:")

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
        
        st.sidebar.title('Filtro de Vendedores')
        
         # Lista de vendedores única do DataFrame
        vendedores_unicos = st.session_state.df['Vendedor'].unique()

        # Multiselect para seleção de vendedores
        filtro_vendedor = st.sidebar.multiselect('Selecione os Vendedores:', vendedores_unicos)

        # Aplica o filtro, se selecionado
        if filtro_vendedor:
            st.session_state.df_filtrado = st.session_state.df[st.session_state.df['Vendedor'].isin(filtro_vendedor)]

            # Calcula a receita total apenas para o vendedor selecionado
            receita_total_vendedor = st.session_state.df_filtrado['Preço'].sum()
            st.success(f"Receita total para {', '.join(filtro_vendedor)}: {format_number(receita_total_vendedor, 'R$')}")
        else:
            st.session_state.df_filtrado = None  # Sem filtro, define como None

        # Exibe o DataFrame filtrado apenas se algum filtro estiver sendo aplicado
        if st.session_state.df_filtrado is not None:
            st.dataframe(st.session_state.df_filtrado)
                
        # Nova Venda
        st.sidebar.title("Adicionar Nova Venda")

        nome_produto = st.sidebar.text_input("Nome do Produto:")
        
        categorias = ["Livros", "Instrumentos musicais", "Brinquedos", "Eletrônicos", "Eletrodomésticos", "Esporte e Lazer"]
        categoria_produto = st.sidebar.selectbox("Categoria do Produto:", categorias)
        
        preco_produto = st.sidebar.number_input("Preço:")
        frete_produto = st.sidebar.number_input("Frete:")
        data_produto = st.sidebar.date_input("Data da Compra:")
        vend_produto = st.sidebar.text_input("Nome do Vendedor:")
        
        ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        local_compra = st.sidebar.selectbox("Local da Compra:", ufs)
        
        av_prod = st.sidebar.selectbox("Avaliação da Compra:", list(range(1, 11)))
        
        opcoes_pagamento = ["cartao_credito", "cartao_debito", "pix"]
        tipo_pagamento = st.sidebar.selectbox("Tipo de Pagamento:", opcoes_pagamento)
        quantidade_parcelas = st.sidebar.selectbox('Quantidade de Parcelas:', list(range(1, 13)))

        latitude = st.sidebar.number_input("Latitude:")
        longitude = st.sidebar.number_input("Longitude:")
        
        campos_preenchidos = nome_produto and categoria_produto and preco_produto and frete_produto and data_produto and vend_produto and local_compra and av_prod and tipo_pagamento and quantidade_parcelas
        
        if campos_preenchidos and st.sidebar.button("Confirmar Nova Venda"):
        # Verifica se a conexão foi estabelecida com sucesso
            if st.session_state.conectado:
                try:
                    # Utiliza a conexão existente
                    conexao = criar_conexao(st.session_state.senha)
                    
                    if conexao is not None:           
                        # Cria uma instância do objeto 'insert' do SQLAlchemy para a tabela "Compra"
                        tabela_compra = insert(Compra).values({
                            'Produto': nome_produto,
                            'Categoria_do_Produto': categoria_produto,
                            'Preço': preco_produto,
                            'Frete': frete_produto,
                            'Data_da_Compra': data_produto,
                            'Vendedor': vend_produto,
                            'Local_da_Compra': local_compra,
                            'Avaliaçao_da_Compra': av_prod,
                            'Tipo_de_Pagamento': tipo_pagamento,
                            'Quantidade_de_Parcelas': quantidade_parcelas,
                            'Latitude': latitude,
                            'Longitude': longitude
                        })

                        # Executa a instrução SQL de INSERT
                        conexao.execute(tabela_compra)
                        
                        conexao.commit()

                        # Recarrega o DataFrame após a inserção para refletir as alterações
                        st.session_state.df = obter_dataframe_conectado(conexao)

                        # Exibe mensagem de sucesso
                        st.warning("Venda adicionada com sucesso!")
                    else:
                        st.warning("Conexão com o banco de dados não está mais válida. Tente reconectar.")
                except Exception as e:
                    st.warning(f"Erro ao adicionar nova venda: {str(e)}")
            else:
                st.warning("Conexão com o banco de dados não foi estabelecida. Por favor, conecte-se antes de adicionar uma nova venda.")
        
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
