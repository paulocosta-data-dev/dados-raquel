import pandas as pd
import os

def atualizar_parquet_com_intervalo(ficheiro_parquet, df_novo, coluna_data):
    """
    Atualiza um ficheiro Parquet removendo as linhas que caem no intervalo de datas
    do novo DataFrame e adicionando os novos dados.

    Parâmetros:
    - ficheiro_parquet (str): caminho para o ficheiro Parquet.
    - df_novo (pd.DataFrame): DataFrame com os novos dados.
    - coluna_data (str): nome da coluna com datas (ex: 'Data').

    Retorna:
    - df_final (pd.DataFrame): DataFrame resultante.
    """

    if df_novo.empty:
        raise ValueError("O DataFrame de novos dados está vazio.")

    min_data = df_novo[coluna_data].min()
    max_data = df_novo[coluna_data].max()

    if os.path.exists(ficheiro_parquet):
        df_existente = pd.read_parquet(ficheiro_parquet)

        df_existente = df_existente[
            ~((df_existente[coluna_data] >= min_data) & (df_existente[coluna_data] <= max_data))
        ]

        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        df_final.to_parquet(ficheiro_parquet, index=False)

        print(f"✅ Substituídas transações de {min_data.date()} a {max_data.date()} em: {ficheiro_parquet}")
    else:
        df_novo.to_parquet(ficheiro_parquet, index=False)
        df_final = df_novo
        print(f"✅ Novo ficheiro parquet criado: {ficheiro_parquet}")

    return df_final