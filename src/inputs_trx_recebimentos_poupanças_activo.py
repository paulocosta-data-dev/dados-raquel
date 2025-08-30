import pandas as pd
import os
import glob
import datetime

from utils.categorias_loader import carregar_categorias
from utils.parquet import atualizar_parquet_com_intervalo
from utils.categorizar_despesa import categorizar_despesa
from utils.exportacao import exportar_descricoes_em_falta  # <- NOVO
from config import PATHS  # importa o dicionário de paths

# --- Configurações ---
conta_nome = 1

pasta_trx = PATHS["pasta_trx"]
pasta_output = PATHS["pasta_output"]
ficheiro_parquet = PATHS["ficheiro_parquet"]
pasta_faltas = PATHS["pasta_faltas"]  # <- NOVO
categorias = carregar_categorias(PATHS["categorias_yaml"])

# --- Encontra o ficheiro Excel mais recente ---
ficheiros = glob.glob(os.path.join(pasta_trx, "*.xlsx"))
if not ficheiros:
    raise FileNotFoundError(f"Nenhum ficheiro .xlsx encontrado em {pasta_trx}")
ficheiro_mais_recente = max(ficheiros, key=os.path.getctime)

# --- Lê o Excel ---
df = pd.read_excel(ficheiro_mais_recente, skiprows=7, header=0)
df = df.rename(columns={'Data Lanc.': 'Data'})

# --- Cria colunas Débito/Crédito ---
df['Débito'] = df['Valor'].apply(lambda x: abs(x) if x < 0 else 0)
df['Crédito'] = df['Valor'].apply(lambda x: x if x > 0 else 0)
df.drop(columns=['Valor', 'Data Valor'], inplace=True)

# --- Adiciona coluna "conta" ---
df['conta'] = conta_nome

# --- Move saldo para último ---
colunas = [col for col in df.columns if col != 'Saldo']
df = df[colunas + ['Saldo']]

# --- Categoriza descrições (primeira fase, por descrição apenas) ---
descricao_df = df[['Descrição']].drop_duplicates().reset_index(drop=True)
descricao_df[['id_categoria', 'categoria']] = descricao_df['Descrição'].apply(
    lambda x: pd.Series(categorizar_despesa(x, categorias=categorias))
)
df = df.merge(descricao_df, on='Descrição', how='left')

# --- Segunda fase: reclassifica os 99 com data e valor ---
df_99 = df[df['id_categoria'] == 99].copy()
if not df_99.empty:
    df_99['valor_total'] = df_99['Débito'] + df_99['Crédito']
    df_99[['id_categoria', 'categoria']] = df_99.apply(
        lambda row: pd.Series(categorizar_despesa(
            row['Descrição'],
            data=row['Data'],
            valor=row['valor_total'],
            categorias=categorias
        )),
        axis=1
    )
    df_99.drop(columns='valor_total', inplace=True)
    df.update(df_99)

# --- Exporta descrições ainda não categorizadas (com função reutilizável) ---
df_sem_categoria = df[df['id_categoria'] == 99]
if not df_sem_categoria.empty:
    exportar_descricoes_em_falta(
        df_sem_categoria,
        conta_nome=conta_nome,
        pasta_faltas=pasta_faltas,
        colunas_exportar=['Data', 'Descrição', 'Débito', 'Crédito', 'Saldo'],
        parar_script=True  # <-- importante para interromper execução
    )

# --- Define colunas finais e atualiza parquet ---
colunas_finais = ['Data', 'id_categoria', 'Débito', 'Crédito', 'Saldo', 'conta']
df_final = df[colunas_finais].copy()
df_final = atualizar_parquet_com_intervalo(ficheiro_parquet, df_final, coluna_data='Data')