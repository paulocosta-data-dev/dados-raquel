@echo off
REM Caminho absoluto para o projeto
SET PROJECT_DIR=C:\Users\pdcge\OneDrive\Documents\git repos\dados-raquel

REM Ativa o ambiente virtual
call "%PROJECT_DIR%\venv\Scripts\activate.bat"

REM Vai para o diretório do projeto
cd /d "%PROJECT_DIR%"

REM Corre a app Streamlit
streamlit run streamlit_make_ui.py
