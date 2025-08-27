# src/utils/categorias.py

CATEGORIAS = [
    {'id': 1, 'nome': 'cabeleireiro', 'padroes': ['BELEZA']},
    {'id': 2, 'nome': 'psicologo',  'padroes': ['TRF P/ NUNO J. SOUSA']},
    {'id': 3, 'nome': 'levantamentos_a_dinheiro', 'padroes': ['LEV ATM']},
    {'id': 4, 'nome': 'pensões', 'padroes': ['ORDENADO', 'CGA PENS', 'APOSENTAC', 'INSTITUTO DE GEST O FINANCE']},
    {'id': 5, 'nome': 'acertos_de_jose_carlos', 'padroes': ['TRF. P/O JOSE CARLOS ABREU FERNANDES']},
    {'id': 6, 'nome': 'supermercado', 'padroes': ['CONTINENTE', 'PINGO DOCE', 'LIDL', 'MINIPRECO', 'SOGENAVE VENDING', 'CONTIN BOM DIA']},
    {'id': 7, 'nome': 'farmacia_e_suplementos', 'padroes': ['FARMACIA', 'WELLS', 'CELEIRO', 'Acerto vaselina amazon']},
    {'id': 8, 'nome': 'restaurantes', 'padroes': ['RESTAURANTE', 'PITADAS', 'TOUCINHO', 'DOM LEIT']},
    {'id': 9, 'nome': 'papelaria_e_livros', 'padroes': ['PAPELARIA']},
    {'id': 10, 'nome': 'chines', 'padroes': ['ZHENG', 'XUEQIAN']},
    {'id': 11, 'nome': 'tech_software', 'padroes': ['APPLE.COM']},
    {'id': 12, 'nome': 'transportes', 'padroes': ['CP', 'ENTRECAMPOS', 'ALVERCA']},
    {'id': 13, 'nome': 'condominio_casa', 'padroes': ['CONDOMINIO PREDIO ENCOSTA SOL']},
    {'id': 14, 'nome': 'tech_hardware', 'padroes': ['RADIO POPULAR']},
    {'id': 15, 'nome': 'estadias_feira_nova', 'padroes': ['TRF P/ JOSE FERNANDES']},
    {'id': 16, 'nome': 'reforço_fundo_emprestimo_casa', 'padroes': ['3302971348']},
    {'id': 17, 'nome': 'transferencia_para_conta_despesas', 'padroes': ['TRF P/ PAULO COSTA']},
    {'id': 99, 'nome': 'outros', 'padroes': []},
]

def categorizar(descricao):
    desc = descricao.upper()
    for categoria in CATEGORIAS:
        if any(p in desc for p in categoria['padroes']):
            return categoria['id'], categoria['nome']
    return 99, 'outros'