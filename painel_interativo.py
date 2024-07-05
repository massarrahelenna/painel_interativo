import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Configuração do tema
st.set_page_config(page_title="O que faz um país próspero?", layout="wide")
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #FFFFFF;
}
.sidebar .sidebar-content {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# Verifique se o arquivo CSV está presente no diretório
file_name = 'trabalho.csv'
current_directory = os.getcwd()
file_path = os.path.join(current_directory, file_name)

if os.path.exists(file_path):
    # Carregue o arquivo CSV para um dataframe
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()
else:
    st.error(f"Arquivo '{file_name}' não encontrado no diretório: {current_directory}")
    st.stop()

# Explicações dos filtros
filtro_descriptions = {
    'HDI': 'Índice de Desenvolvimento Humano (IDH) que mede o desenvolvimento humano com base em saúde, educação e padrão de vida.',
    'DBS': 'Índice de Facilidade de Fazer Negócios que avalia a facilidade com que as empresas podem operar em um país.',
    'GCI': 'Índice de Competitividade Global que mede a capacidade de um país fornecer um ambiente sustentável para a prosperidade econômica.',
    'GDP': 'Produto Interno Bruto (PIB) que mede o valor de mercado de todos os bens e serviços finais produzidos em um país.',
    'Tax/GDP': 'Taxa de Impostos sobre o PIB que indica a proporção do PIB de um país que é arrecadada como imposto pelo governo.',
    'GII': 'Índice de Inovação Global que avalia a capacidade de um país em incentivar e facilitar a inovação.',
    'RND': 'Gastos em Pesquisa e Desenvolvimento como proporção do PIB, um indicador chave para inovação e desenvolvimento tecnológico.',
    'EDS': 'Medidas educacionais como taxa de alfabetização, média de anos de escolaridade, qualidade do sistema educacional, etc.',
    'GE': 'Métricas de igualdade de gênero em diferentes aspectos sociais e econômicos.',
    'CPI': 'Índice de Percepção de Corrupção que avalia o nível de corrupção percebida no setor público de um país.',
    'GINI': 'Coeficiente de Gini que mede a desigualdade de renda dentro de um país.',
    'WHS': 'Índice de Felicidade Mundial que mede a felicidade percebida com base em vários fatores.',
    'SPS': 'Índice de Progresso Social que avalia o bem-estar social de um país com base em necessidades humanas básicas e inclusão.'
}

# Verificar se df foi carregado corretamente
if not df.empty:
    # Filtros e seleção de países
    filtros = st.sidebar.multiselect(
        "Escolha os filtros",
        options=list(filtro_descriptions.keys()),
        format_func=lambda x: filtro_descriptions[x]
    )

    paises = st.sidebar.multiselect(
        "Escolha os países",
        options=df['Country'].unique().tolist()
    )

    # Se nenhum filtro selecionado, exibir estatísticas gerais em gráfico de linhas
    if not filtros:
        st.subheader("Estatísticas Gerais")

        # Gráfico de linhas para estatísticas gerais
        if st.button("Mostrar Estatísticas Gerais"):
            fig = go.Figure()
            for filtro, descricao in filtro_descriptions.items():
                if filtro in df.columns:
                    fig.add_trace(go.Scatter(x=df['Country'], y=df[filtro], mode='lines', name=filtro))
            fig.update_layout(title='Estatísticas Gerais por Categoria', xaxis_title='Países', yaxis_title='Valor', template='plotly_dark')
            st.plotly_chart(fig)

    # Se filtros selecionados, exibir dados específicos por país em gráficos de pizza
    if filtros and paises:
        # Aplicando os filtros e seleção de países
        df_selecionado = df[df['Country'].isin(paises)]

        # Plotar gráficos de pizza para dados específicos por país
        st.subheader("Dados Específicos por País")
        for filtro in filtros:
            st.write(f"### {filtro_descriptions[filtro]}")
            if filtro in df_selecionado.columns:
                try:
                    fig = px.pie(df_selecionado, names='Country', values=filtro, title=f"{filtro} por País")
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(showlegend=True, template='plotly_dark')
                    st.plotly_chart(fig)
                except ValueError:
                    st.warning(f"Não foi possível plotar o gráfico de pizza para '{filtro}'. Verifique se os dados são válidos.")
            else:
                st.warning(f"Coluna '{filtro}' não encontrada nos dados selecionados.")

    elif filtros or paises:
        st.warning("Selecione pelo menos um filtro e país para visualizar os gráficos.")

else:
    st.warning("Por favor, selecione pelo menos um filtro e país para visualizar os gráficos.")
