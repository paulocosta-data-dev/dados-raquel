import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Paths e colunas ---
BASE_PATH = r"C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\processed\meta"
CAMINHO_DESPESAS = os.path.join(BASE_PATH, "despesas_manuais.parquet")
CAMINHO_CAIXA = os.path.join(BASE_PATH, "fundo_caixa.parquet")
CAMINHO_CATEGORIAS = os.path.join(BASE_PATH, "dim_categorias.parquet")

COLUNAS = ["Data", "Categoria", "Descrição", "Valor (€)"]

# --- Garantir que a pasta existe ---
os.makedirs(BASE_PATH, exist_ok=True)

# --- Função para carregar parquet (não cria ficheiro) ---
@st.cache_data
def carregar_parquet(caminho):
    if os.path.exists(caminho):
        return pd.read_parquet(caminho)
    else:
        return pd.DataFrame(columns=COLUNAS)

# --- Guardar parquet (cria ficheiro só ao salvar o df) ---
def guardar_parquet(df, caminho):
    # Aqui não criamos ficheiro vazio antecipadamente
    df.to_parquet(caminho, index=False)

# --- Carregar categorias --- (sem alterações)
@st.cache_data
def carregar_categorias():
    if os.path.exists(CAMINHO_CATEGORIAS):
        df_cat = pd.read_parquet(CAMINHO_CATEGORIAS)
        if 'id_categoria' in df_cat.columns and 'categoria' in df_cat.columns:
            return df_cat[['id_categoria', 'categoria']].drop_duplicates().sort_values('id_categoria')
        else:
            st.error("O ficheiro de categorias está num formato inesperado.")
            return pd.DataFrame(columns=['id_categoria', 'categoria'])
    else:
        st.warning("Ficheiro de categorias não encontrado.")
        return pd.DataFrame(columns=['id_categoria', 'categoria'])

# --- Carregar dados ---
df_despesas = carregar_parquet(CAMINHO_DESPESAS)
df_caixa = carregar_parquet(CAMINHO_CAIXA)
categorias = carregar_categorias()

# --- Filtrar categoria para fundo de caixa (id 3) ---
categoria_caixa = categorias[categorias['id_categoria'] == 3]
cat_caixa_nome = categoria_caixa['categoria'].values[0] if not categoria_caixa.empty else "levantamentos_a_dinheiro"

# --- Setup da página ---
st.set_page_config(page_title="Gestão de Despesas e Fundo de Caixa", layout="wide")
st.title("💸 Gestão de Despesas Manuais e Fundo de Caixa")

# --- Tabs principais ---
tabs = st.tabs(["➕ Adicionar Registo", "📋 Visualizar/Editar Dados", "⚙️ Gerir Dados"])

# ========== TAB 1: Adicionar Registo ==========
with tabs[0]:
    st.subheader("Adicionar novo registo")
    tipo = st.radio("Escolha o tipo de registo:", options=["Despesa Manual", "Fundo de Caixa"])

    with st.form("form_adicionar"):
        data = st.date_input("Data", value=date.today())
        
        if tipo == "Despesa Manual":
            categorias_despesas = categorias[categorias['id_categoria'] != 3]
            lista_categorias = categorias_despesas['categoria'].tolist()
            categoria_selecionada = st.selectbox("Categoria", options=lista_categorias)
        else:
            categoria_selecionada = cat_caixa_nome
            st.text_input("Categoria", value=categoria_selecionada, disabled=True)

        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (€)", min_value=0.01, format="%.2f")
        submitted = st.form_submit_button("Adicionar")

        if submitted:
            if not descricao.strip():
                st.error("⚠️ A descrição não pode ficar vazia.")
            else:
                nova_linha = pd.DataFrame([{
                    "Data": pd.to_datetime(data),
                    "Categoria": categoria_selecionada.strip(),
                    "Descrição": descricao.strip(),
                    "Valor (€)": round(valor, 2)
                }])

                if tipo == "Despesa Manual":
                    if df_despesas.empty:
                        # Ficheiro não existe ou está vazio, então começamos um novo df
                        df_despesas = nova_linha
                    else:
                        df_despesas = pd.concat([df_despesas, nova_linha], ignore_index=True)
                    guardar_parquet(df_despesas, CAMINHO_DESPESAS)
                else:
                    if df_caixa.empty:
                        df_caixa = nova_linha
                    else:
                        df_caixa = pd.concat([df_caixa, nova_linha], ignore_index=True)
                    guardar_parquet(df_caixa, CAMINHO_CAIXA)

                st.success("✅ Registo adicionado com sucesso!")
