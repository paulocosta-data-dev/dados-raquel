import yaml

def carregar_categorias(path_yaml):
    with open(path_yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
