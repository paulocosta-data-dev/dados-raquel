import pandas as pd

def categorizar_despesa(descricao, data=None, valor=None, categorias=None):
    desc = descricao.upper()
    data_str = pd.to_datetime(data).strftime('%Y-%m-%d') if data else None
    valor_rounded = round(valor, 2) if valor is not None else None

    for cat in categorias:
        padroes = cat.get("padroes", [])
        datas = cat.get("datas", [])
        valores = cat.get("valores", [])

        padrao_match = any(p.upper() in desc for p in padroes) if padroes else True
        data_match = data_str in datas if datas and data_str else True
        valor_match = valor_rounded in valores if valores and valor_rounded is not None else True

        if padrao_match and data_match and valor_match:
            return cat["id"], cat["nome"]

    return 99, "outros"