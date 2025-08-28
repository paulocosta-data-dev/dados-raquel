import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Configuração ---
CAMINHO_PARQUET = r"C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\processed\meta\despesas_manuais.parquet"
CAMINHO_CATEGORIAS = r"C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\processed\meta\dim_categorias.parquet"
COLUNAS = ["Data", "Categoria", "Descrição", "Valor (€)"]

# --- Função para carregar despesas ---
@st.cache_data
def carregar_despesas():
    if os.path.exists(CAMINHO_PARQUET):
        return pd.read_parquet(CAMINHO_PARQUET)
    else:
        return pd.DataFrame(columns=COLUNAS)

# --- Função para carregar categorias ---
@st.cache_data
def carregar_categorias():
    if os.path.exists(CAMINHO_CATEGORIAS):
        df_cat = pd.read_parquet(CAMINHO_CATEGORIAS)
        return sorted(df_cat['categoria'].dropna().unique())
    else:
        return []

# --- Função para guardar ---
def guardar_despesas(df):
    df.to_parquet(CAMINHO_PARQUET, index=False)

# --- Carregamento inicial ---
df = carregar_despesas()
lista_categorias = carregar_categorias()

# --- Título ---
st.set_page_config(page_title="Despesas Manuais", layout="wide")
st.title("💸 Gestão de Despesas Manuais")

# --- Tabs ---
tabs = st.tabs(["➕ Nova Despesa", "📋 Ver Despesas", "⚙️ Gerir Dados"])

# ==============================
# 🟢 TAB 1: Adicionar nova despesa
# ==============================
with tabs[0]:
    st.subheader("Adicionar nova despesa")

    with st.form("form_despesa"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", value=date.today())

            if lista_categorias:
                categoria = st.selectbox("Categoria", options=lista_categorias)
            else:
                st.warning("⚠️ Nenhuma categoria encontrada. Verifique o ficheiro de categorias.")
                categoria = st.text_input("Categoria (manual)")

        with col2:
            descricao = st.text_input("Descrição")
            valor = st.number_input("Valor (€)", min_value=0.01, format="%.2f")

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            if not categoria or not descricao:
                st.error("⚠️ Todos os campos devem ser preenchidos.")
            else:
                nova = pd.DataFrame([{
                    "Data": pd.to_datetime(data),
                    "Categoria": categoria.strip().title(),
                    "Descrição": descricao.strip(),
                    "Valor (€)": round(valor, 2)
                }])

                df = pd.concat([df, nova], ignore_index=True)
                guardar_despesas(df)
                st.success("✅ Despesa adicionada com sucesso!")

# ==============================
# 🟠 TAB 2: Visualizar tabela
# ==============================
with tabs[1]:
    st.subheader("Despesas registadas")

    if df.empty:
        st.info("Nenhuma despesa registada.")
    else:
        df_ordenado = df.sort_values("Data", ascending=False).reset_index(drop=True)
        st.dataframe(df_ordenado, use_container_width=True)

        with st.expander("📤 Exportar"):
            col1, col2 = st.columns(2)
            with col1:
                csv = df_ordenado.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ CSV", csv, file_name="despesas_manuais.csv", mime="text/csv")
            with col2:
                excel = df_ordenado.to_excel(index=False, engine='openpyxl')
                st.download_button("⬇️ Excel", excel, file_name="despesas_manuais.xlsx")

# ==============================
# 🔴 TAB 3: Limpar base de dados
# ==============================
with tabs[2]:
    st.subheader("Gerir dados")

    with st.expander("⚠️ Apagar todas as despesas"):
        apagar = st.checkbox("Confirmo que quero apagar todos os dados.")
        if st.button("Apagar tudo", disabled=not apagar):
            df = pd.DataFrame(columns=COLUNAS)
            guardar_despesas(df)
            st.success("🗑️ Todas as despesas foram apagadas com sucesso.")
