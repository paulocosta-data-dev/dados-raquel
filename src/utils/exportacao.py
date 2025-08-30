import os
import pandas as pd

def exportar_descricoes_em_falta(df_sem_categoria, conta_nome, pasta_faltas, colunas_exportar, parar_script=True):
    """
    Exporta descrições não categorizadas para Excel. Se o ficheiro já existir, junta os novos registos.

    Parâmetros:
    - df_sem_categoria: DataFrame com descrições não categorizadas
    - conta_nome: nome da conta (usado no nome do ficheiro)
    - pasta_faltas: diretório onde guardar o ficheiro
    - colunas_exportar: lista de colunas a exportar
    - parar_script: se True, faz exit(1) ao terminar
    """
    os.makedirs(pasta_faltas, exist_ok=True)
    
    data_hoje = pd.Timestamp.now().strftime('%Y%m%d')
    ficheiro_faltas = os.path.join(pasta_faltas, f'descrições_em_falta_{conta_nome}_{data_hoje}.xlsx')

    df_exportar = df_sem_categoria[colunas_exportar].drop_duplicates().copy()
    df_exportar['Data'] = pd.to_datetime(df_exportar['Data']).dt.date

    while True:
        try:
            if os.path.exists(ficheiro_faltas):
                df_existente = pd.read_excel(ficheiro_faltas)
                df_novo = pd.concat([df_existente, df_exportar], ignore_index=True)
                df_novo = df_novo.drop_duplicates(subset=colunas_exportar)
                df_novo.to_excel(ficheiro_faltas, index=False)
                print(f"⚠️ Ficheiro existente atualizado: {ficheiro_faltas}")
            else:
                df_exportar.to_excel(ficheiro_faltas, index=False)
                print(f"⚠️ Descrições em falta exportadas: {ficheiro_faltas}")
            break
        except PermissionError:
            print(f"\n❌ Ficheiro {ficheiro_faltas} está aberto. Fecha-o e prima ENTER para tentar novamente...")
            input()

    if parar_script:
        print("\n⛔ Existem descrições por categorizar. O script vai parar para permitir correção.")
        exit(1)