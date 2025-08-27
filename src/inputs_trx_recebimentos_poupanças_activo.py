import pandas as pd
import os
import glob
import datetime
from utils.categorias import categorizar
from utils.categorias_contexto import categorizar_por_contexto
from utils.parquet import atualizar_parquet_com_intervalo

# --- Configurações ---
conta_nome = 'recebimentos_poupanças'
pasta_trx = r'C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\raw\trx\recebimentos_poupanças'
pasta_output = r'C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\processed\trx\recebimentos_poupanças'
ficheiro_parquet = os.path.join(pasta_output, f'{conta_nome}.parquet')

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

# --- Categoriza descrições ---
descricao_df = df[['Descrição']].drop_duplicates().reset_index(drop=True)
descricao_df[['id_categoria', 'categoria']] = descricao_df['Descrição'].apply(lambda x: pd.Series(categorizar(x)))
df = df.merge(descricao_df, on='Descrição', how='left')

# --- Reclassifica os 99 com categorização por contexto ---
df_99 = df[df['id_categoria'] == 99].copy()
if not df_99.empty:
    df_99['valor_total'] = df_99['Débito'] + df_99['Crédito']
    df_99[['id_categoria', 'categoria']] = df_99.apply(
        lambda row: pd.Series(categorizar_por_contexto(row['Data'], row['Descrição'], row['valor_total'])),
        axis=1
    )
    df_99.drop(columns='valor_total', inplace=True)
    df.update(df_99)

# --- Exporta descrições ainda não categorizadas ---
df_sem_categoria = df[df['id_categoria'] == 99]
if not df_sem_categoria.empty:
    # Apaga ficheiros Excel antigos na pasta de output
    ficheiros_excel = glob.glob(os.path.join(pasta_output, '*.xlsx'))
    for f in ficheiros_excel:
        try:
            os.remove(f)
        except PermissionError:
            print(f"\n❌ Não foi possível apagar o ficheiro porque está aberto: {f}")
            input("🔒 Por favor, feche o ficheiro e prima ENTER para continuar...")
            os.remove(f)

    # Cria novo ficheiro com data no nome
    data_hoje = datetime.datetime.now().strftime('%Y%m%d')
    path_faltas = os.path.join(
        pasta_output,
        f'descrições_em_falta_{conta_nome}_{data_hoje}.xlsx'
    )
    colunas_exportar = ['Data', 'Descrição', 'Débito', 'Crédito', 'Saldo']

    try:
        df_exportar = df_sem_categoria[colunas_exportar].drop_duplicates().copy()
        df_exportar['Data'] = df_exportar['Data'].dt.date  # <-- apenas data
        df_exportar.to_excel(path_faltas, index=False)
        print(f"⚠️ Descrições não categorizadas exportadas para: {path_faltas}")
    except PermissionError:
        print(f"\n❌ Não foi possível escrever o ficheiro porque está aberto: {path_faltas}")
        input("🔒 Por favor, feche o ficheiro e prima ENTER para tentar novamente...")
        df_exportar.to_excel(path_faltas, index=False)
        print(f"✅ Ficheiro guardado após nova tentativa: {path_faltas}")

# --- Define colunas finais ---
colunas_finais = ['Data', 'id_categoria', 'Débito', 'Crédito', 'Saldo', 'conta']
df_final = df[colunas_finais].copy()

# --- Atualiza ficheiro parquet com base no intervalo de datas ---
df_final = atualizar_parquet_com_intervalo(ficheiro_parquet, df_final, coluna_data='Data')