# src/utils/categorias_contexto.py

import pandas as pd
from datetime import datetime

CATEGORIAS_CONTEXTO = [
    {
        'id': 2,
        'nome': 'psicologo',
        'padroes': ['TRF P/ Poupancas'],
        'datas': [],
        'valores': [70]
    },
    
    
    {
        'id': 6,
        'nome': 'supermercado',
        'padroes': ['TRF P/ Mae Poupancas', 'TRF DE PAULO FRANCISCO P A FERNANDES COSTA'],
        'datas': [],
        'valores': [93.83, 119.3, 53.62, 49.9]
    },
    
        {
        'id': 8,
        'nome': 'restaurantes',
        'padroes': ['TRF P/ Mae Poupancas'],
        'datas': [],
        'valores': [92.09]
    },
    
        {
        'id': 7,
        'nome': 'farmacia_e_suplementos',
        'padroes': ['TRF P/ Poupancas', 'TRF. P/O PAULO FRANCISCO P A FERNANDES COSTA', 'TRF P/ Mae Poupancas'],
        'datas': [],
        'valores': [28.98, 51.44, 12.20, 95.41, 52.61, 71.12, 50.26, 65.64, 44.92, 21.7, 52.15]
    },
    
    {
        'id': 7,
        'nome': 'farmacia_e_suplementos',
        'padroes': ['Acerto vaselina amazon'],
        'datas': ['2025-04-11'],
        'valores': [0.16]
    },
    
    {
        'id': 16,
        'nome': 'reforço_fundo_emprestimo_casa',
        'padroes': ['TRF. P/O PAULO FRANCISCO P A FERNANDES COSTA', 'TRF. P/O  PAULO FRANCISCO P A FERNAND'],
        'datas': [],
        'valores': [70, 200]
    },
    
    {
        'id': 17,
        'nome': 'transferencia_para_conta_despesas',
        'padroes': ['TRF P/ PAULO FRANCISCO P A FERNANDES COSTA'],
        'datas': ['2025-07-17'],
        'valores': [150]
    },

    {
        'id': 227,
        'nome': 'seguro_casa',
        'padroes': ['TRF P/ Poupancas'],
        'datas': ['2025-04-22'],
        'valores': [191.39]
    },    

    
    
    {
        'id': 228,
        'nome': 'utilização_fundo_imprevistos',
        'padroes': ['TRF P/ Mae Poupancas'],
        'datas': ['2025-07-21'],
        'valores': [300, 325]
    },
    

        
        
    {
        'id': 229,
        'nome': 'compras_pessoais',
        'padroes': ['TRF P/ Mae Poupancas', 'TRF. P/O PAULO FRANCISCO P A FERNANDES COSTA'],
        'datas': ['2025-06-02'],
        'valores': [269.87]
    },
    
    
    {
        'id': 229,
        'nome': 'utilizacao_fundo_emprestimo_casa',
        'padroes': ['TRF P/ PAULO FRANCISCO P A FERNANDES COSTA'],
        'datas': [],
        'valores': [5500]
    },
    
    {
        'id': 99,
        'nome': 'outros',
        'padroes': [],
        'datas': [],
        'valores': []
    }
]


def categorizar_por_contexto(data, descricao, valor_total):
    desc = descricao.upper()
    data_str = pd.to_datetime(data).strftime('%Y-%m-%d')

    for categoria in CATEGORIAS_CONTEXTO:
        padroes_match = any(p.upper() in desc for p in categoria['padroes']) if categoria['padroes'] else True
        data_match = data_str in categoria['datas'] if categoria['datas'] else True
        valor_match = round(valor_total, 2) in categoria['valores'] if categoria['valores'] else True

        if padroes_match and data_match and valor_match:
            return categoria['id'], categoria['nome']

    return 99, 'outros'
