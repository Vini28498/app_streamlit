# Importing libs
import streamlit as st
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

# Create page title
st.set_page_config(page_title="titulo_da_pagina")

# Create title
with st.container():
    st.title("titulo_do_app")
    st.write("descricao_do_app")

    # Criar um DataFrame com múltiplas linhas
    df4 = pd.DataFrame({
        "latitude": ['coordenadas_lat'],                  # Gráfico de Mapas
        "longitude": ['coordenadas_lon']
    })

    # Criar o mapa com base no DataFrame
    st.map(df4, latitude='latitude', longitude='longitude', zoom=14.5)

    st.write("---")   

# Crendentials database
def conectar_bd():
    conn = psycopg2.connect(
        host="seu_host",
        database="seu_banco_de_dados",
        user="seu_usuario",
        password="sua_senha"
    )
    return conn

# Coneccting database
conn = conectar_bd()

# Schema and table name
schema = "seu_esquema"
nome_tabela = "nome_da_tabela"

# Reading second table
def tabela2(conn, schema, nome_tabela):
    cur = conn.cursor()
    cur.execute(f"instrucao_sql{schema}.{nome_tabela}")
    rows = cur.fetchall()

    # Obter nomes de coluna
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{nome_tabela}'")
    columns = [col[0] for col in cur.fetchall()]

    # Criar DataFrame
    df = pd.DataFrame(rows, columns=["colunas"])

    return df

# Create second chart
with st.container():
    st.subheader('titulo_kpi', divider='rainbow')
    df2 = tabela2(conn, schema, nome_tabela)
    print(df2)

    for index, row in df2.iterrows():               ### Métricas de KPI's
        valor = row['column1']
        st.metric(label=row['column2'], value=valor)

# Reading first table
def tabela1(conn, schema, nome_tabela):
    cur = conn.cursor()
    cur.execute(f"instrucao_sql{schema}.{nome_tabela}")
    rows = cur.fetchall()

    # Obter nomes de coluna
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{nome_tabela}'")
    columns = [col[0] for col in cur.fetchall()]

    # Criar DataFrame
    df = pd.DataFrame(rows, columns=["colunas"])

    return df

# Create first chart
with st.container():
    st.write("---")

    df1 = tabela1(conn, schema, nome_tabela)
    print(df1)
                                               ### Grafíco de Barras
    st.subheader("titulo_do_grafico")                  
    st.bar_chart(df1, x="column1", y="column2")

# Reading first table
def tabela3(conn, schema, nome_tabela):
    cur = conn.cursor()
    cur.execute(f"instrucao_sql{schema}.{nome_tabela}")
    rows = cur.fetchall()

    # Obter nomes de coluna
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{nome_tabela}'")
    columns = [col[0] for col in cur.fetchall()]

    # Criar DataFrame
    df = pd.DataFrame(rows, columns=["colunas"])

    return df

def main():
    st.write('---')
    st.subheader("titulo_do_grafico")

    # Carregar os dados
    df = tabela3(conn, schema, nome_tabela)

    # Criar seletor de ano
    anos_disponiveis = df['ano'].unique()
    ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis)

    # Filtrar os dados de acordo com o ano selecionado
    df_filtrado = df[df['ano'] == ano_selecionado]                 ### Gráfico de Linhas clusterizado por mes e ano.

    # Ordenar os meses
    meses_ordenados = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_filtrado['mes'] = pd.Categorical(df_filtrado['mes'], categories=meses_ordenados, ordered=True)
    df_filtrado = df_filtrado.sort_values('mes')

    # Mostrar o gráfico de linhas
    st.line_chart(df_filtrado.set_index('mes')['total'], use_container_width=True, width=2, color='#ffaa00')

if __name__ == "__main__":
    main()
