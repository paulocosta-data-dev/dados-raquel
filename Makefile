# Caminhos dos executáveis do venv
PYTHON=.\venv\Scripts\python.exe
STREAMLIT=.\venv\Scripts\streamlit.exe
PIP=.\venv\Scripts\pip.exe

# Pastas
SRC_DIR=src
META_DIR=data/processed/meta
RAW_OUTPUT_DIR=data/processed/trx/recebimentos_poupanças

# ---------------------
# AJUDA
# ---------------------
help:
	@echo ""
	@echo "📘 Comandos disponíveis:"
	@echo "  make setup           - Cria o ambiente virtual e instala dependências"
	@echo "  make run-app         - Inicia a aplicação Streamlit (input manual)"
	@echo "  make categorias      - Gera o ficheiro categorias.parquet"
	@echo "  make recebimentos    - Corre script de recebimentos (poupanças)"
	@echo "  make transacoes      - Executa todos os scripts de transações"
	@echo "  make all             - Executa categorias, transações e app"
	@echo "  make clean           - Remove ficheiros temporários e excels gerados"
	@echo "  make clean-venv      - Apaga o ambiente virtual (⚠️ permanente)"
	@echo ""

# ---------------------
# Alvos principais
# ---------------------

setup:
	python -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run-app:
	$(STREAMLIT) run $(SRC_DIR)/manual_input_app.py

categorias:
	$(PYTHON) $(SRC_DIR)/categorias_tabela.py

recebimentos:
	$(PYTHON) $(SRC_DIR)/recebimentos_poupanças.py

transacoes: recebimentos
	@echo "✅ Todos os scripts de transações foram executados."

all: categorias transacoes run-app

# ---------------------
# Limpeza
# ---------------------

clean:
	@echo "🧹 A limpar ficheiros temporários..."
	-del /q /s __pycache__ > nul 2>&1
	-rd /s /q __pycache__ > nul 2>&1
	-del /q $(RAW_OUTPUT_DIR)\*.xlsx > nul 2>&1
	-del /q $(META_DIR)\*.parquet > nul 2>&1
	@echo "🧼 Limpeza concluída."

clean-venv:
	-rd /s /q venv
	@echo "🗑️ Ambiente virtual removido."