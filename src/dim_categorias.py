import pandas as pd
import os
from utils.categorias_loader import carregar_categorias  # Importa o loader do YAML
from config import PATHS

# --- Carrega as categorias do YAML unificado ---
categorias_unificadas = carregar_categorias(PATHS["categorias_yaml"])

# --- Extrai só id e nome ---
def extrair_id_nome(lista_categorias):
    return [(cat["id"], cat["nome"]) for cat in lista_categorias]

valores = extrair_id_nome(categorias_unificadas)

# --- Remove duplicados e ordena por id ---
df_categorias = pd.DataFrame(valores, columns=["id_categoria", "categoria"])
df_categorias = df_categorias.drop_duplicates().sort_values("id_categoria").reset_index(drop=True)

# --- Define pasta e ficheiro de saída ---
pasta_output = PATHS["output_meta"]
os.makedirs(pasta_output, exist_ok=True)

ficheiro_parquet = os.path.join(pasta_output, "dim_categorias.parquet")

# --- Guarda o ficheiro parquet ---
df_categorias.to_parquet(ficheiro_parquet, index=False)
print(f"✅ Ficheiro de categorias guardado em: {ficheiro_parquet}")
