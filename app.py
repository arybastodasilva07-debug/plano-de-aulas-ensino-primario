import streamlit as st
import os
import json

st.set_page_config(page_title="Plataforma Pedagógica Angola", layout="wide")

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================

PASTA_DOCS = "documentos_oficiais"
FAVORITOS_FILE = "favoritos.json"

if not os.path.exists(PASTA_DOCS):
    os.makedirs(PASTA_DOCS)

if not os.path.exists(FAVORITOS_FILE):
    with open(FAVORITOS_FILE, "w") as f:
        json.dump({}, f)

# =========================
# FUNÇÕES AUXILIARES
# =========================

def carregar_favoritos():
    with open(FAVORITOS_FILE, "r") as f:
        return json.load(f)

def salvar_favoritos(dados):
    with open(FAVORITOS_FILE, "w") as f:
        json.dump(dados, f)

# =========================
# LOGIN SIMPLES
# =========================

st.sidebar.title("🔐 Login")

usuario = st.sidebar.text_input("Nome do utilizador")

if usuario:
    st.sidebar.success(f"Bem-vindo, {usuario}")

# =========================
# MENU PRINCIPAL
# =========================

menu = st.sidebar.radio("Menu", ["🏠 Início", "📚 Biblioteca Oficial"])

# =========================
# INÍCIO
# =========================

if menu == "🏠 Início":
    st.title("🇦🇴 Plataforma Pedagógica Digital")
    st.subheader("Ensino Primário - Angola")
    st.write("Sistema oficial de apoio ao professor.")

# =========================
# BIBLIOTECA OFICIAL
# =========================

elif menu == "📚 Biblioteca Oficial":

    st.title("📚 Biblioteca Oficial")

    aba1, aba2 = st.tabs(["📎 Upload (Admin)", "📂 Documentos"])

    # -----------------------
    # ABA UPLOAD (ADMIN)
    # -----------------------
    with aba1:
        senha_admin = st.text_input("Senha de Administrador", type="password")

        if senha_admin == "admin123":

            st.subheader("Adicionar Documento Oficial")

            titulo = st.text_input("Título do Documento")
            classe = st.selectbox("Classe", 
                                  ["Iniciação", "1ª Classe", "2ª Classe",
                                   "3ª Classe", "4ª Classe", 
                                   "5ª Classe", "6ª Classe"])

            disciplina = st.text_input("Disciplina")
            tipo_doc = st.selectbox("Tipo de Documento",
                                    ["Programa Oficial",
                                     "Livro do Aluno",
                                     "Guia Metodológico",
                                     "Manual do Professor"])

            uploaded_file = st.file_uploader(
                "Anexar documento (PDF ou DOCX)",
                type=["pdf", "docx"]
            )

            if st.button("Guardar Documento"):
                if uploaded_file and titulo:
                    nome_final = f"{classe}_{disciplina}_{titulo}_{uploaded_file.name}"
                    caminho = os.path.join(PASTA_DOCS, nome_final)

                    with open(caminho, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.success("Documento guardado com sucesso!")
                else:
                    st.warning("Preencha todos os campos.")

        else:
            st.info("Área restrita ao administrador.")

    # -----------------------
    # ABA DOCUMENTOS
    # -----------------------
    with aba2:

        favoritos = carregar_favoritos()

        if usuario and usuario not in favoritos:
            favoritos[usuario] = []
            salvar_favoritos(favoritos)

        filtro_classe = st.selectbox("Filtrar por Classe",
                                     ["Todas", "Iniciação", "1ª Classe",
                                      "2ª Classe", "3ª Classe",
                                      "4ª Classe", "5ª Classe",
                                      "6ª Classe"])

        mostrar_favoritos = st.checkbox("Mostrar apenas favoritos")

        arquivos = os.listdir(PASTA_DOCS)

        for arquivo in arquivos:

            if filtro_classe != "Todas" and not arquivo.startswith(filtro_classe):
                continue

            if mostrar_favoritos and usuario:
                if arquivo not in favoritos.get(usuario, []):
                    continue

            st.divider()
            col1, col2, col3 = st.columns([4,1,1])

            col1.write(f"📄 {arquivo}")

            # Visualizar PDF online
            if arquivo.endswith(".pdf"):
                with open(os.path.join(PASTA_DOCS, arquivo), "rb") as f:
                    col2.download_button(
                        "📥 Baixar",
                        f,
                        file_name=arquivo
                    )
            else:
                with open(os.path.join(PASTA_DOCS, arquivo), "rb") as f:
                    col2.download_button(
                        "📥 Baixar",
                        f,
                        file_name=arquivo
                    )

            # Favoritos
            if usuario:
                if arquivo in favoritos.get(usuario, []):
                    if col3.button("⭐ Remover", key=arquivo):
                        favoritos[usuario].remove(arquivo)
                        salvar_favoritos(favoritos)
                        st.rerun()
                else:
                    if col3.button("☆ Favoritar", key=arquivo):
                        favoritos[usuario].append(arquivo)
                        salvar_favoritos(favoritos)
                        st.rerun()

