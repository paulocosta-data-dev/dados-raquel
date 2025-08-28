import pandas as pd
import os

# --- Importa os dicionários de categorias ---
from utils.categorias import CATEGORIAS as categorias_simples
from utils.categorias_contexto import CATEGORIAS_CONTEXTO as categorias_contexto

# --- Extrai apenas id e nome de cada categoria ---
def extrair_id_nome(lista_categorias):
    return [(cat["id"], cat["nome"]) for cat in lista_categorias]

valores_1 = extrair_id_nome(categorias_simples)
valores_2 = extrair_id_nome(categorias_contexto)

# --- Junta, remove duplicados e ordena ---
todas_categorias = valores_1 + valores_2
df_categorias = pd.DataFrame(todas_categorias, columns=["id_categoria", "categoria"])
df_categorias = df_categorias.drop_duplicates().sort_values("id_categoria").reset_index(drop=True)

# --- Define pasta e ficheiro de saída ---
pasta_output = os.path.join("data", "processed", "meta")
os.makedirs(pasta_output, exist_ok=True)

ficheiro_parquet = os.path.join(pasta_output, "dim_categorias.parquet")

# --- Guarda o ficheiro parquet ---
df_categorias.to_parquet(ficheiro_parquet, index=False)
print(f"✅ Ficheiro de categorias guardado em: {ficheiro_parquet}")
