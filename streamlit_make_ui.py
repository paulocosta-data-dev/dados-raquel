import streamlit as st
import subprocess
import os
import re
import locale

# --- Configuração ---
MAKEFILE_PATH = "Makefile"
MAKE_EXEC = r"C:\ProgramData\chocolatey\bin\make.exe"

# --- Extrai os targets do Makefile ---
def extrair_targets(makefile_path):
    targets = []
    if not os.path.exists(makefile_path):
        st.error(f"❌ Makefile não encontrado em: `{makefile_path}`")
        return targets

    try:
        with open(makefile_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r'^([a-zA-Z0-9\-_]+)\s*:', line)
                if m:
                    targets.append(m.group(1))
        return list(sorted(set(targets)))
    except Exception as e:
        st.error(f"Erro ao ler Makefile: {e}")
        return []

# --- Executa o target ---
def run_make(target):
    try:
        encoding = locale.getpreferredencoding()
        result = subprocess.run(
            [MAKE_EXEC, target],
            capture_output=True,
            encoding=encoding,
            errors='replace',
            shell=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", f"Erro ao executar make: {e}"

# --- Interface Principal ---
def main():
    st.set_page_config(page_title="Executar Makefile", page_icon="🛠️", layout="centered")
    st.title("🛠️ Interface Gráfica para Makefile")
    st.caption("Clica num dos comandos abaixo para executar")

    targets = extrair_targets(MAKEFILE_PATH)

    if not targets:
        st.warning("⚠️ Nenhum target encontrado.")
        return

    col1, col2 = st.columns(2)
    resultado = None
    erro = None
    target_executado = None

    for i, target in enumerate(targets):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"▶️ {target}"):
            target_executado = target
            with st.spinner(f"Executando `make {target}`..."):
                resultado, erro = run_make(target)

    if target_executado:
        st.success(f"✅ Target `{target_executado}` executado com sucesso.")

        tabs = st.tabs(["📤 Output", "❌ Erros"])
        with tabs[0]:
            st.text_area("Saída (stdout)", resultado or "Sem saída.", height=300)
        with tabs[1]:
            st.text_area("Erros (stderr)", erro or "Sem erros.", height=200)

    st.divider()
    with st.expander("ℹ️ Sobre esta app"):
        st.markdown("""
        - Interface leve para executar comandos definidos no `Makefile`
        - Ideal para tarefas como: gerar dados, correr scripts, iniciar apps
        - Caminho para o make:  
          `C:\\ProgramData\\chocolatey\\bin\\make.exe`
        """)

if __name__ == "__main__":
    main()
