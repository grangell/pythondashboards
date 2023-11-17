import plotly.express as px

def criar_grafico_map_estado(df_rec_estado):
    grafico_map_estado = px.scatter_geo(
        df_rec_estado,
        lat='Latitude',
        lon='Longitude',
        scope = 'south america',
        size='Preço',
        template='seaborn',
        hover_name='Local da Compra',
        hover_data={'Latitude': False, 'Longitude': False},
        title='Receita por Estado',
    )
    grafico_map_estado.update_geos(projection_type="equirectangular")
    return grafico_map_estado
    
def criar_grafico_rec_mensal(df_rec_mensal):
    grafico_rec_mensal = px.line(
        df_rec_mensal,
        x = 'Mes',
        y = 'Preço',
        markers = True,
        range_y = (0, df_rec_mensal.max()),
        color = 'Ano',
        line_dash = 'Ano',
        title = 'Receita Mensal',
    )
    grafico_rec_mensal.update_layout(yaxis_title = 'Receita')
    return grafico_rec_mensal
    
def criar_grafico_rec_estado(df_rec_estado):
    grafico_rec_estado = px.bar(
        df_rec_estado.head(7),
        x = 'Local da Compra',
        y = 'Preço',
        text_auto = True,
        title = 'Top Receitas por Estados'    
    )
    return grafico_rec_estado

def criar_grafico_rec_categoria(df_rec_categoria):
    grafico_rec_categoria = px.bar(
        df_rec_categoria.head(7),
        text_auto = True,
        title = 'Receita por Categoria'
    )
    return grafico_rec_categoria

def criar_grafico_rec_vendedores(df_vendedores):
    grafico_rec_vendedores = px.bar(
        df_vendedores[['sum']].sort_values('sum', ascending=False).head(7),
        x = 'sum',
        y = df_vendedores[['sum']].sort_values('sum', ascending=False).head(7).index,
        text_auto = True,
        title = 'Top 7 Vendedores por Receita',
    )
    return grafico_rec_vendedores

def criar_grafico_vendas_vendedores(df_vendedores):
    grafico_rec_top7 = px.bar(
        df_vendedores[['count']].sort_values('count', ascending=False).head(7),
        x = 'count',
        y = df_vendedores[['count']].sort_values('count', ascending=False).head(7).index,
        text_auto = True,
        title = 'Top 7 Vendedores por Venda'
    )
    return grafico_rec_top7