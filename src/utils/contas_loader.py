import yaml
import pandas as pd
import os

def carregar_contas(path_yaml):
    with open(path_yaml, "r", encoding="utf-8") as f:
        dados = yaml.safe_load(f)
    return pd.DataFrame(dados["contas"])