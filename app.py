import streamlit as st
import sqlite3
import hashlib
import os

st.set_page_config(page_title="Plataforma Pedagógica Angola", layout="wide")

# =========================
# BASE DE DADOS
# =========================

conn = sqlite3.connect("plataforma.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha TEXT,
    tipo TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    classe TEXT,
    disciplina TEXT,
    tipo TEXT,
    nome_arquivo TEXT
)
""")

conn.commit()

# =========================
# FUNÇÃO HASH SENHA
# =========================

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# =========================
# SESSÃO
# =========================

if "logado" not in st.session_state:
    st.session_state.logado = False

# =========================
# REGISTO / LOGIN
# =========================

if not st.session_state.logado:

    aba1, aba2 = st.tabs(["🔐 Login", "📝 Registar"])

    # LOGIN
    with aba1:
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE email=? AND senha=?",
                      (email, hash_senha(senha)))
            user = c.fetchone()

            if user:
                st.session_state.logado = True
                st.session_state.usuario_id = user[0]
                st.session_state.usuario_nome = user[1]
                st.session_state.tipo = user[4]
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    # REGISTO
    with aba2:
        nome = st.text_input("Nome completo")
        email_reg = st.text_input("Email")
        senha_reg = st.text_input("Senha", type="password")

        if st.button("Criar Conta"):
            try:
                c.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                          (nome, email_reg, hash_senha(senha_reg), "professor"))
                conn.commit()
                st.success("Conta criada com sucesso!")
            except:
                st.error("Email já existe")

# =========================
# ÁREA LOGADA
# =========================

else:

    st.sidebar.success(f"👤 {st.session_state.usuario_nome}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    menu = st.sidebar.radio("Menu", ["🏠 Início", "📚 Biblioteca"])

    if menu == "🏠 Início":
        st.title("🇦🇴 Plataforma Pedagógica Digital")
        st.subheader("Sistema Nacional de Apoio ao Professor")

    if menu == "📚 Biblioteca":

        st.title("📚 Biblioteca Oficial")

        # ADMIN pode adicionar
        if st.session_state.tipo == "admin":

            st.subheader("Adicionar Documento Oficial")

            titulo = st.text_input("Título")
            classe = st.selectbox("Classe",
                                  ["Iniciação", "1ª Classe", "2ª Classe",
                                   "3ª Classe", "4ª Classe",
                                   "5ª Classe", "6ª Classe"])
            disciplina = st.text_input("Disciplina")
            tipo_doc = st.selectbox("Tipo",
                                    ["Programa Oficial",
                                     "Livro do Aluno",
                                     "Guia Metodológico"])

            uploaded_file = st.file_uploader("PDF ou DOCX", type=["pdf", "docx"])

            if st.button("Guardar Documento"):
                if uploaded_file:

                    pasta = "documentos_oficiais"
                    if not os.path.exists(pasta):
                        os.makedirs(pasta)

                    caminho = os.path.join(pasta, uploaded_file.name)

                    with open(caminho, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    c.execute("""
                    INSERT INTO documentos (titulo, classe, disciplina, tipo, nome_arquivo)
                    VALUES (?, ?, ?, ?, ?)
                    """, (titulo, classe, disciplina, tipo_doc, uploaded_file.name))

                    conn.commit()
                    st.success("Documento adicionado!")

        # TODOS podem visualizar
        st.subheader("Documentos Disponíveis")

        c.execute("SELECT * FROM documentos")
        docs = c.fetchall()

        for doc in docs:
            st.divider()
            st.write(f"📄 {doc[1]}")
            st.write(f"{doc[2]} | {doc[3]} | {doc[4]}")

            with open(f"documentos_oficiais/{doc[5]}", "rb") as f:
                st.download_button("📥 Baixar", f, file_name=doc[5])
