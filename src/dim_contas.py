import pandas as pd
import os
from utils.contas_loader import carregar_contas
from config import PATHS

# --- Carrega contas do YAML ---
contas = carregar_contas(PATHS["dim_contas_yaml"])
df_dim_contas = pd.DataFrame(contas)

# --- Guarda o ficheiro na pasta definida em config ---
pasta_meta = PATHS["pasta_meta"]
os.makedirs(pasta_meta, exist_ok=True)

df_dim_contas.to_parquet(os.path.join(pasta_meta, "dim_contas.parquet"), index=False)
print("✅ dim_contas.parquet criado a partir de YAML.")