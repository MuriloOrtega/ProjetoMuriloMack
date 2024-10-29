import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Função para exibir os dados de origem carregados
def dados_origem(data):
    """
    Exibe os dados de origem em uma tabela interativa no Streamlit.
    
    Parâmetros:
    data (DataFrame): Dados a serem exibidos.
    """
    st.subheader("Dados de origem")
    st.dataframe(data)

# Função para exibir a contagem de pessoas por gênero
def exibir_gen(data):
    """
    Exibe um gráfico de barras com a contagem de pessoas por gênero.
    
    Parâmetros:
    data (DataFrame): Dados contendo informações de gênero.
    """
    # Gera um dataset de contagem de gêneros
    gender_counts = data['gender'].value_counts().rename_axis('gender').reset_index(name='counts')
    gender_counts.set_index('gender', inplace=True)

    # Gráfico do número de pessoas por gênero
    st.divider()
    st.subheader("Número de pessoas por gênero")
    st.bar_chart(gender_counts['counts'], x_label="Gêneros", y_label="Quantidade")

# Função para exibir a média de anos de educação por gênero
def gen_edu(data):
    """
    Exibe um gráfico de barras com a média de anos de educação por gênero.
    
    Parâmetros:
    data (DataFrame): Dados contendo informações de gênero e anos de educação.
    """
    # Gera um dataset de média de anos de educação por gênero
    gender_education_mean = data.groupby('gender')['years_of_education'].mean().reset_index(name='means')
    gender_education_mean.set_index('gender', inplace=True)

    # Gráfico da média de anos de educação
    st.divider()
    st.subheader("Média de anos trabalhados")
    st.bar_chart(gender_education_mean['means'], color="#00aa00", x_label="Gênero", y_label="Média de anos trabalhados")

# Função para exibir a distribuição do status de emprego
def gen_empg(data):
    """
    Exibe um gráfico de pizza com a distribuição do status de emprego.
    
    Parâmetros:
    data (DataFrame): Dados contendo informações de status de emprego.
    """
    # Gera um dataset de contagem do status de emprego
    job_counts = data['employment_status'].value_counts().rename_axis('employment_status').reset_index(name='counts')
    job_counts.set_index('employment_status', inplace=True)

    # Gráfico de pizza do Status de Emprego no Streamlit com o Plotly
    st.divider()
    st.subheader("Distribuição do Status de Emprego")
    fig = px.pie(job_counts, values='counts', names=job_counts.index)
    st.plotly_chart(fig)

# Função para criar faixas etárias e exibir a distribuição de idade
def gen_did(data):
    """
    Cria faixas etárias e calcula a distribuição geral por idade.
    
    Parâmetros:
    data (DataFrame): Dados contendo informações de idade.
    """
    # Cria faixas etárias
    data['age_group'] = pd.cut(data['age'], bins=[0, 18, 30, 45, 60, 100], labels=['0-18', '19-30', '31-45', '46-60', '61+'])

    # Distribuição geral por idade
    age_group_counts = data['age_group'].value_counts().sort_index()

# Função para exibir o número de pessoas por geração
def gen_act(data):
    """
    Exibe um gráfico de barras horizontal com o número de pessoas por geração.
    
    Parâmetros:
    data (DataFrame): Dados contendo informações de geração.
    """
    # Gera um dataset de contagem de geração
    generation_counts = data['generation'].value_counts().rename_axis('generation').reset_index(name='counts')
    generation_counts.set_index('generation', inplace=True)

    # Gráfico do número de pessoas por geração (horizontal)
    st.divider()
    st.subheader("Número de pessoas por geração")
    st.bar_chart(generation_counts['counts'], color="#ffaa00", x_label="Geração", y_label="Quantidade", horizontal=True)

# Configuração do título da janela
st.set_page_config(page_title="Indicadores referente ao arquivo CSV", page_icon="👁")
try:
    # Leitura do arquivo CSV contendo os dados
    file = '/workspaces/ProjetoMuriloMack/APP/persons.csv'
    data = pd.read_csv(file)
except Exception as e:
    st.info("Arquivo não encontrado")
# Processamento dos dados

# Criação de faixas etárias para distribuição de idade
data['age_group'] = pd.cut(data['age'], bins=[0, 18, 30, 45, 60, 100], labels=['0-18', '19-30', '31-45', '46-60', '61+'])
age_group_counts = data['age_group'].value_counts().sort_index()

# Distribuição de idade e gênero
age_gender_distribution = data.groupby(['age_group', 'gender'], observed=True).size().unstack(fill_value=0)

# Renderizações no Streamlit
st.title("Indicadores referente ao arquivo CSV")

dados_origem(data)
exibir_gen(data)
gen_edu(data)
gen_empg(data)
gen_did(data)
gen_act(data)

# Mostra o histograma geral de idades
st.divider()
st.subheader("Distribuição por Idade")
fig_grouped_age = px.bar(age_group_counts, labels={"value": "Número de Pessoas", "variable": "Idade"}, barmode='stack')
fig_grouped_age.update_layout(xaxis_title="Idades")
st.plotly_chart(fig_grouped_age)

# Mostra o histograma geral de idades agrupado por gênero
st.divider()
st.subheader("Distribuição por Idade e Gênero")
fig_grouped_gen = px.bar(age_gender_distribution, labels={"value": "Número de Pessoas", "variable": "Idade"}, barmode='group')
fig_grouped_gen.update_layout(xaxis_title="Idades")
st.plotly_chart(fig_grouped_gen)
