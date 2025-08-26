import pandas as pd
import os
import glob

# Caminho da pasta onde o ficheiro está localizado
pasta = r'C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel\data\raw\trx'

# Encontra o ficheiro Excel mais recente na pasta
ficheiros = glob.glob(os.path.join(pasta, "*.xlsx"))
ficheiro_mais_recente = max(ficheiros, key=os.path.getctime)

# Lê o ficheiro Excel
df = pd.read_excel(ficheiro_mais_recente, skiprows=7, header=0)

# Exibe as primeiras linhas do dataframe (para depuração)
print(f"Ficheiro lido: {ficheiro_mais_recente}")

# Cria as colunas "Débito" e "Crédito"
df['Débito'] = df['Valor'].apply(lambda x: abs(x) if x < 0 else 0)  # Remove o sinal negativo da coluna 'Débito'
df['Crédito'] = df['Valor'].apply(lambda x: x if x > 0 else 0)

# Remove as colunas 'Valor' e 'Data Valor'
df = df.drop(columns=['Valor', 'Data Valor'])

# Renomeia a coluna 'Data Lanc.' para 'Data trx'
df = df.rename(columns={'Data Lanc.': 'Data trx'})

# Move a coluna 'Saldo' para a última posição
colunas = [col for col in df.columns if col != 'Saldo']
colunas.append('Saldo')
df = df[colunas]
print(df.head(15))

# Dicionário de categorias com ID, nome e padrões
CATEGORIAS = [
    {'id': 1, 'nome': 'cabeleireiro', 'padroes': ['BELEZA']},
    {'id': 2, 'nome': 'psicólogo',  'padroes': ['TRF P/ NUNO J. SOUSA']},
    {'id': 3, 'nome': 'levantamentos_a_dinheiro', 'padroes': ['LEV ATM']},
    {'id': 4, 'nome': 'pensões',     'padroes': ['ORDENADO', 'CGA PENS', 'APOSENTAC', 'INSTITUTO DE GEST O FINANCE']},
    {'id': 5, 'nome': 'acertos_de_jose_carlos',    'padroes': ['TRF. P/O JOSE CARLOS ABREU FERNANDES']},
    {'id': 6, 'nome': 'supermercado', 'padroes': ['CONTINENTE', 'PINGO DOCE', 'LIDL', 'MINIPRECO', 'SOGENAVE VENDING', 'CONTIN']},
    {'id': 7, 'nome': 'farmacia_e_suplementos',     'padroes': ['FARMACIA', 'WELLS', 'CELEIRO', 'Acerto vaselina amazon']},
    {'id': 8, 'nome': 'restaurantes',  'padroes': ['RESTAURANTE', 'PITADAS', 'TOUCINHO', 'DOM LEIT']},
    {'id': 9, 'nome': 'papelaria_e_livros',    'padroes': ['PAPELARIA']},
    {'id': 10, 'nome': 'chines',    'padroes': ['ZHENG', 'XUEQIAN']},
    {'id': 11,'nome': 'tech_software',         'padroes': ['APPLE.COM']},
    {'id': 12,'nome': 'transportes',  'padroes': ['CP', 'ENTRECAMPOS', 'ALVERCA']},
    {'id': 13, 'nome': 'condominio_casa', 'padroes': ['CONDOMINIO PREDIO ENCOSTA SOL']},
    {'id': 14, 'nome': 'tech_hardware', 'padroes': ['RADIO POPULAR']},
    {'id': 15, 'nome': 'estadias_feira_nova', 'padroes': ['TRF P/ JOSE FERNANDES']},
    {'id': 16, 'nome': 'reforco_fundo_emprestimo_casa', 'padroes': ['REFORCO AUT CDA']},
    {'id': 99,'nome': '',       'padroes': []},
]

# Função para categorizar a descrição e devolver (id_categoria, nome_categoria)
def categorizar(descricao):
    desc = descricao.upper()
    for categoria in CATEGORIAS:
        if any(p in desc for p in categoria['padroes']):
            return categoria['id'], categoria['nome']
    return 99, 'outros'

# Isola descrições únicas e aplica categorização
descricao_df = (
    df[['Descrição']]
    .drop_duplicates()
    .reset_index(drop=True)
    .copy()
)
descricao_df[['id_categoria', 'categoria']] = descricao_df['Descrição'].apply(lambda x: pd.Series(categorizar(x)))

# Adiciona um índice inteiro único para cada descrição
descricao_df['id_descricao'] = descricao_df.index + 1
descricao_df['id_descricao'] = descricao_df['id_descricao'].astype('int64')

# Junta as categorias e id_descricao ao dataframe principal
df = df.merge(descricao_df, on='Descrição', how='left')

# Mostra algumas linhas para verificação
#print(df[['Data trx', 'id_categoria', 'categoria', 'Débito', 'Crédito', 'Saldo']].head(15))

# === Filtrar transações sem categoria (id_categoria == 99) ===
df_sem_categoria = df[df['id_categoria'] == 99]

# Conta quantas transações não têm categoria
num_sem_categoria = df_sem_categoria.shape[0]

print(f"\nNúmero de transações sem categoria: {num_sem_categoria}")

print("\nTransações sem categoria:")
print(df_sem_categoria[['Data trx', 'Descrição', 'Débito', 'Crédito', 'Saldo']].head(60))
