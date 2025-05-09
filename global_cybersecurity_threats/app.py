import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel de Cibersegurança", layout="wide")
st.title("🔐 Painel de Incidentes de Cibersegurança (últimos anos)")

@st.cache_data
def carregar_dados():
    df = pd.read_csv(r"data/dados.csv")  # Substitua pelo nome correto do arquivo

    return df

df = carregar_dados()

with st.sidebar:
    st.header("Filtros")
    paises = st.multiselect("País", df["Country"].unique(), default=df["Country"].unique())
    tipos = st.multiselect("Tipo de Ataque", df["Attack Type"].unique(), default=df["Attack Type"].unique())
    anos = st.slider("Ano", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))

df_filtro = df[
    (df["Country"].isin(paises)) &
    (df["Attack Type"].isin(tipos)) &
    (df["Year"].between(anos[0], anos[1]))
]

col1, col2, col3 = st.columns(3)
col1.metric("🔢 Incidentes", len(df_filtro))
col2.metric("💸 Perda Total (Mi USD)", f"${df_filtro['Financial Loss (in Million $)'].sum():,.2f}")
col3.metric("👥 Usuários Afetados", f"{df_filtro['Number of Affected Users'].sum():,}")

st.divider()

df_pais = df_filtro["Country"].value_counts().reset_index()
df_pais.columns = ["País", "Incidentes"]
fig1 = px.bar(df_pais, x="País", y="Incidentes", text="Incidentes", title="Incidentes por País", template="plotly")
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

df_ano = df_filtro.groupby("Year")["Financial Loss (in Million $)"].sum().reset_index()
fig2 = px.line(df_ano, x="Year", y="Financial Loss (in Million $)", markers=True, title="Perda Financeira ao Longo do Tempo", template="plotly")
fig2.update_traces(text=df_ano["Financial Loss (in Million $)"].round(2).astype(str), textposition="top center")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(df_filtro, names="Attack Type", title="Distribuição por Tipo de Ataque", template="plotly")
st.plotly_chart(fig3, use_container_width=True)

st.download_button("📥 Baixar dados filtrados", data=df_filtro.to_csv(index=False).encode(), file_name="dados_filtrados.csv")

st.info("Fonte: [Kaggle - Global Cybersecurity Threats 2015-2024](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)")