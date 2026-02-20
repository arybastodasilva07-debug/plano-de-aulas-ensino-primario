========================
ARQUIVO: requirements.txt
========================
streamlit
python-docx
reportlab


========================
ARQUIVO: disciplinas.py
========================
disciplinas = {
    "Iniciação": [
        "Iniciação à Leitura e Escrita",
        "Matemática",
        "Estudo do Meio",
        "Expressão Plástica",
        "Expressão Musical"
    ],
    "1ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio"],
    "2ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio"],
    "3ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia"],
    "4ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia"],
    "5ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia"],
    "6ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia"]
}


========================
ARQUIVO: gerador_ia.py
========================
def gerar_plano(dados):

    plano = f"""
🇦🇴 PLANO DE AULA – ENSINO PRIMÁRIO (INIDE)

Classe: {dados['classe']}
Disciplina: {dados['disciplina']}
Tema: {dados['tema']}
Sumário: {dados['subtema']}
Tempo: {dados['tempo']}
Aula Nº: {dados['aula']}

1. OBJECTIVOS GERAIS
- Desenvolver competências previstas no programa do INIDE.
- Promover valores de cidadania e responsabilidade.

2. OBJECTIVOS DA AULA
- Identificar conceitos principais sobre {dados['subtema']}.
- Relacionar o conteúdo com situações da vida na comunidade.

3. CONTEÚDO
- Conceito e explicação do tema.
- Exemplos práticos da realidade angolana.

4. MATERIAL DIDÁCTICO
- Quadro e giz
- Manual escolar
- Objectos locais
- Cartolinas

5. METODOLOGIA
- Método participativo
- Trabalho em grupo
- Perguntas orientadoras

6. ACTIVIDADES-CHAVE
- Discussão inicial
- Exercício prático
- Apresentação em grupo

7. AVALIAÇÃO
- Observação directa
- Participação
- Exercícios escritos

8. TAREFA PARA CASA
- Realizar exercícios do manual.
- Pesquisar exemplos na comunidade.
"""

    return plano


========================
ARQUIVO: exportador.py
========================
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import io


def exportar_word(texto):
    doc = Document()
    doc.add_paragraph(texto)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream


def exportar_pdf(texto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph(texto.replace("\n", "<br/>"), styles["Normal"]))
    doc.build(elements)
    buffer.seek(0)
    return buffer


========================
ARQUIVO: app.py
========================
import streamlit as st
from disciplinas import disciplinas
from gerador_ia import gerar_plano
from exportador import exportar_word, exportar_pdf

st.set_page_config(page_title="Plano de Aula PRO 🇦🇴", layout="wide")

st.title("🇦🇴 PLATAFORMA PROFISSIONAL DE PLANOS DE AULA")
st.markdown("Baseado no Programa Oficial do INIDE")

col1, col2 = st.columns([1,2])

with col1:
    st.header("📘 Dados da Aula")
    classe = st.selectbox("Classe", list(disciplinas.keys()))
    disciplina = st.selectbox("Disciplina", disciplinas[classe])
    tema = st.text_input("Tema")
    subtema = st.text_input("Sumário")
    tempo = st.text_input("Tempo")
    aula = st.number_input("Aula Nº", min_value=1, step=1)

    gerar = st.button("🚀 Gerar Plano")

with col2:
    if gerar:
        dados = {
            "classe": classe,
            "disciplina": disciplina,
            "tema": tema,
            "subtema": subtema,
            "tempo": tempo,
            "aula": aula
        }

        plano = gerar_plano(dados)

        st.success("Plano gerado com sucesso!")
        st.text_area("Plano de Aula", plano, height=600)

        colw, colp = st.columns(2)

        with colw:
            st.download_button(
                "📄 Baixar Word",
                exportar_word(plano),
                file_name="plano_de_aula.docx"
            )

        with colp:
            st.download_button(
                "📕 Baixar PDF",
                exportar_pdf(plano),
                file_name="plano_de_aula.pdf"
)
