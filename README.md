# 💳 Data Pipeline Bancário (Python + DuckDB + dbt)

Este projeto implementa um pipeline de dados bancários totalmente **gratuito**, com Python para extração, DuckDB como data warehouse, dbt para transformação/testes, e integração com Power Query / Excel.

---

## 🚀 Setup do Ambiente

### 1. Clonar o repositório
```bash
git clone https://github.com/teu-user/teu-repo.git
cd teu-repo
```

### 2. Criar e ativar ambiente virtual
No Windows PowerShell:
```powershell
python -m venv venv
.env\Scriptsctivate
```

No Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

---

## 🛠️ Fluxo do Pipeline

1. **Extract**  
   - Script Python lê ficheiros bancários `.xlsx`/`.xls`  
   - Exporta para ficheiros `.parquet` (armazenados local ou em cloud storage)

2. **Load**  
   - DuckDB lê diretamente os `.parquet` como tabelas externas  
   - Fácil integração via DBeaver ou Power Query

3. **Transform + Test (dbt)**  
   - dbt executa transformações SQL sobre DuckDB  
   - Validações automáticas com dbt tests (ex.: categorias válidas, ids não nulos)

4. **Consume**  
   - Conectar Excel / Power BI / Power Query diretamente ao DuckDB ou aos `.parquet`

---

## 📦 Comandos Essenciais

Ativar ambiente:
```powershell
.env\Scriptsctivate   # Windows
source venv/bin/activate  # Linux/Mac
```

Atualizar dependências:
```bash
pip install NOVO_PACOTE
pip freeze > requirements.txt
```

Rodar dbt:
```bash
dbt run
dbt test
```

---

## 📂 Estrutura do Projeto (exemplo)

```
.
├── extract.py           # scripts Python de extração
├── requirements.txt     # dependências do projeto
├── README.md            # este guia
├── data/                # ficheiros .xlsx/.xls originais
├── parquet/             # ficheiros .parquet transformados
└── dbt_project/         # pasta do dbt (models, seeds, tests)
```

---

## ✅ Próximos Passos
- Criar `extract.py` para leitura dos ficheiros bancários
- Definir `seeds/` no dbt para categorias
- Escrever testes dbt (not null, foreign key, etc.)
- Configurar Power Query a apontar para os `.parquet`/DuckDB
