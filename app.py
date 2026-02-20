import streamlit as st
from openai import OpenAI
from docx import Document
from docx.shared import Inches
import io

# CONFIGURAÇÃO
st.set_page_config(page_title="Plano de Aula - INIDE Angola", layout="wide")

st.title("🇦🇴 SISTEMA PROFISSIONAL DE PLANO DE AULA")
st.subheader("Ensino Primário (Iniciação à 6ª Classe)")

# OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🏫 Identificação")

    nome_escola = st.text_input("Nome da Escola")
    nome_professor = st.text_input("Nome do Professor")
    trimestre = st.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
    logotipo = st.file_uploader("Logotipo da Escola (opcional)", type=["png", "jpg", "jpeg"])

    st.header("📚 Dados da Aula")

    disciplina = st.selectbox(
        "Disciplina",
        ["Língua Portuguesa", "Matemática", "Estudo do Meio",
         "Ciências Naturais", "Educação Moral e Cívica",
         "Educação Visual e Plástica", "Educação Física"]
    )

    classe = st.selectbox(
        "Classe",
        ["Iniciação", "1ª Classe", "2ª Classe",
         "3ª Classe", "4ª Classe", "5ª Classe", "6ª Classe"]
    )

    tempo = "45 minutos"
    aula_numero = st.number_input("Aula nº", min_value=1, step=1)

    unidade = st.text_input("Unidade Temática")
    subtema = st.text_input("Subtema / Sumário")

    gerar = st.button("🧠 Gerar Plano de Aula")


# ---------------- FUNÇÃO IA ----------------
def gerar_plano():
    prompt = f"""
    Gere um plano de aula completo baseado no currículo oficial do INIDE (Angola).

    Escola: {nome_escola}
    Professor: {nome_professor}
    Disciplina: {disciplina}
    Classe: {classe}
    Trimestre: {trimestre}
    Tempo: {tempo}
    Aula nº: {aula_numero}
    Unidade temática: {unidade}
    Subtema: {subtema}

    Se o subtema for amplo, divida em mais de uma aula de 45 minutos.

    Estrutura obrigatória:

    1. Objetivo Geral
    2. Objetivos da Aula
    3. Conteúdo
    4. Material Didáctico
    5. Metodologia
    6. Actividades Chave
    7. Tipo de Avaliação
    8. Procedimentos:
        - Introdução
        - Desenvolvimento
        - Consolidação
        - Avaliação
        - Tarefa para Casa

    Linguagem formal pedagógica.
    Contexto angolano.
    """

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Especialista em planos de aula do ensino primário angolano."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    return resposta.choices[0].message.content


# ---------------- GERAR WORD ----------------
def gerar_word(plano_texto):
    doc = Document()

    doc.add_heading("REPÚBLICA DE ANGOLA", level=1)
    doc.add_paragraph(f"Escola: {nome_escola}")
    doc.add_paragraph(f"Professor: {nome_professor}")
    doc.add_paragraph(f"Disciplina: {disciplina}")
    doc.add_paragraph(f"Classe: {classe}")
    doc.add_paragraph(f"Trimestre: {trimestre}")
    doc.add_paragraph(f"Aula nº: {aula_numero}")
    doc.add_paragraph(f"Tempo: {tempo}")
    doc.add_paragraph(" ")

    doc.add_heading("PLANO DE AULA", level=2)
    doc.add_paragraph(plano_texto)

    if logotipo is not None:
        doc.add_picture(logotipo, width=Inches(1.5))

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


# ---------------- EXECUÇÃO ----------------
if gerar:
    if unidade == "" or subtema == "":
        st.warning("⚠️ Preencha Unidade Temática e Subtema.")
    else:
        with st.spinner("Gerando plano profissional..."):
            plano = gerar_plano()

        st.success("✅ Plano gerado com sucesso!")
        st.markdown(plano)

        # Download TXT
        st.download_button(
            "📥 Baixar em TXT",
            plano,
            "plano_de_aula.txt"
        )

        # Download Word
        word_file = gerar_word(plano)
        st.download_button(
            "📄 Baixar em Word (.docx)",
            word_file,
            "plano_de_aula.docx"
        )
