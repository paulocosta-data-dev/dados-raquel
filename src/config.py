# src/config.py

import os

# Base do projeto: duas pastas acima do ficheiro config.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminhos usados no projeto
PATHS = {
    "pasta_trx": os.path.join(BASE_DIR, "data", "raw", "trx", "recebimentos_poupanças"),
    "pasta_output": os.path.join(BASE_DIR, "data", "processed", "trx", "recebimentos_poupanças"),
    "ficheiro_parquet": os.path.join(BASE_DIR, "data", "processed", "trx", "recebimentos_poupanças", "recebimentos_poupanças.parquet"),
    "categorias_yaml": os.path.join(BASE_DIR, "src", "utils", "dados_categorias.yaml"),
    "pasta_faltas": os.path.join(BASE_DIR, "data", "processed", "faltas"),
    "dim_contas_yaml": os.path.join(BASE_DIR, "src", "utils", "contas.yaml"),
    "pasta_meta": os.path.join(BASE_DIR, "data", "processed", "meta"),
}

