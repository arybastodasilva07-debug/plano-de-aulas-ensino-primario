import streamlit as st
import os
import sqlite3

st.set_page_config(page_title="Plataforma Pedagógica Angola", layout="wide")

PASTA_DOCS = "documentos_oficiais"

if not os.path.exists(PASTA_DOCS):
    os.makedirs(PASTA_DOCS)

# =========================
# BASE DE DADOS SQLITE
# =========================

conn = sqlite3.connect("plataforma.db", check_same_thread=False)
c = conn.cursor()

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

c.execute("""
CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    documento_id INTEGER
)
""")

conn.commit()

# =========================
# LOGIN SIMPLES
# =========================

st.sidebar.title("🔐 Login")
usuario = st.sidebar.text_input("Nome do utilizador")

if usuario:
    st.sidebar.success(f"Bem-vindo, {usuario}")

menu = st.sidebar.radio("Menu", ["🏠 Início", "📚 Biblioteca Oficial"])

# =========================
# INÍCIO
# =========================

if menu == "🏠 Início":
    st.title("🇦🇴 Plataforma Pedagógica Digital")
    st.subheader("Ensino Primário - Angola")

# =========================
# BIBLIOTECA
# =========================

elif menu == "📚 Biblioteca Oficial":

    st.title("📚 Biblioteca Oficial")

    aba1, aba2 = st.tabs(["📎 Upload (Admin)", "📂 Documentos"])

    # -------------------------
    # UPLOAD ADMIN
    # -------------------------
    with aba1:

        senha_admin = st.text_input("Senha de Administrador", type="password")

        if senha_admin == "admin123":

            titulo = st.text_input("Título")
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

            uploaded_file = st.file_uploader("Anexar (PDF ou DOCX)", type=["pdf", "docx"])

            if st.button("Guardar Documento"):
                if uploaded_file and titulo:

                    caminho = os.path.join(PASTA_DOCS, uploaded_file.name)

                    with open(caminho, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    c.execute("""
                    INSERT INTO documentos (titulo, classe, disciplina, tipo, nome_arquivo)
                    VALUES (?, ?, ?, ?, ?)
                    """, (titulo, classe, disciplina, tipo_doc, uploaded_file.name))

                    conn.commit()

                    st.success("Documento guardado com sucesso!")

        else:
            st.info("Área restrita ao administrador.")

    # -------------------------
    # LISTAGEM DOCUMENTOS
    # -------------------------
    with aba2:

        filtro_classe = st.selectbox("Filtrar por Classe",
                                     ["Todas", "Iniciação", "1ª Classe",
                                      "2ª Classe", "3ª Classe",
                                      "4ª Classe", "5ª Classe",
                                      "6ª Classe"])

        query = "SELECT * FROM documentos"

        if filtro_classe != "Todas":
            query += " WHERE classe=?"
            c.execute(query, (filtro_classe,))
        else:
            c.execute(query)

        documentos = c.fetchall()

        for doc in documentos:

            doc_id = doc[0]
            titulo = doc[1]
            classe = doc[2]
            disciplina = doc[3]
            tipo = doc[4]
            arquivo = doc[5]

            st.divider()
            col1, col2, col3 = st.columns([4,1,1])

            col1.write(f"📄 {titulo}")
            col1.write(f"Classe: {classe} | Disciplina: {disciplina} | Tipo: {tipo}")

            with open(os.path.join(PASTA_DOCS, arquivo), "rb") as f:
                col2.download_button("📥 Baixar", f, file_name=arquivo)

            if usuario:
                c.execute("SELECT * FROM favoritos WHERE usuario=? AND documento_id=?",
                          (usuario, doc_id))
                fav = c.fetchone()

                if fav:
                    if col3.button("⭐ Remover", key=f"rem_{doc_id}"):
                        c.execute("DELETE FROM favoritos WHERE usuario=? AND documento_id=?",
                                  (usuario, doc_id))
                        conn.commit()
                        st.rerun()
                else:
                    if col3.button("☆ Favoritar", key=f"fav_{doc_id}"):
                        c.execute("INSERT INTO favoritos (usuario, documento_id) VALUES (?, ?)",
                                  (usuario, doc_id))
                        conn.commit()
                        st.rerun()
