import streamlit as st
from openai import OpenAI
from docx import Document
from docx.shared import Inches
import io

# CONFIGURAÇÃO
st.set_page_config(page_title="Plano de Aula - INIDE Angola", layout="wide")
st.title("🇦🇴 SISTEMA PROFISSIONAL DE PLANO DE AULA")
st.subheader("Ensino Primário (Iniciação à 6ª Classe)")

# CLIENTE OPENAI
api_key = None
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    import os
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API Key não configurada. Vá em Settings → Secrets e adicione OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# ------------------ CURRÍCULO (exemplo, você pode expandir) ------------------
curriculo = {
    "4ª Classe": {
        "Matemática": {
            "Operações Básicas": ["Adição com reagrupamento", "Subtração simples"],
            "Geometria": ["Formas planas", "Medidas de comprimento"]
        },
        "Língua Portuguesa": {
            "Leitura": ["Compreensão de texto", "Identificação de personagens"],
            "Gramática": ["Substantivos e adjetivos", "Verbos simples"]
        }
    },
    "5ª Classe": {
        "Matemática": {
            "Frações": ["Identificação de frações", "Comparação de frações"],
            "Geometria": ["Polígonos", "Perímetros"]
        }
    }
}

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("🏫 Identificação")
    nome_escola = st.text_input("Nome da Escola")
    nome_professor = st.text_input("Nome do Professor")
    trimestre = st.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
    logotipo = st.file_uploader("Logotipo da Escola (opcional)", type=["png","jpg","jpeg"])

    st.header("📚 Dados da Aula")
    
    # Menu dependente
    classe = st.selectbox("Classe", list(curriculo.keys()))
    disciplinas = list(curriculo[classe].keys())
    disciplina = st.selectbox("Disciplina", disciplinas)
    
    temas = list(curriculo[classe][disciplina].keys())
    tema = st.selectbox("Tema", temas)
    
    subtemas = curriculo[classe][disciplina][tema]
    subtema = st.selectbox("Subtema", subtemas)
    
    aula_numero = st.number_input("Aula nº", min_value=1, step=1)
    tempo = "45 minutos"
    
    gerar = st.button("🧠 Gerar Plano de Aula")

# ------------------ FUNÇÃO PARA GERAR PLANO ------------------
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
Unidade temática: {tema}
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
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Especialista em planos de aula do ensino primário angolano."},
                {"role":"user","content":prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        return resposta.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Não foi possível gerar o plano. Motivo: {e}")
        st.stop()

# ------------------ FUNÇÃO PARA GERAR WORD ------------------
def gerar_word(plano_texto):
    doc = Document()
    doc.add_heading("REPÚBLICA DE ANGOLA", level=1)
    doc.add_paragraph(f"Escola: {nome_escola}")
    doc.add_paragraph(f"Professor: {nome_professor}")
    doc.add_paragraph(f"Disciplina: {disciplina}")
    doc.add_paragraph(f"Classe: {classe}")
    doc.add_paragraph(f"Trimestre: {trimestre}")
    doc.add_paragraph(f"Aula nº: {aula_numero}")
    doc.add_paragraph(f"Tempo: {tempo}\n")
    doc.add_heading("PLANO DE AULA", level=2)
    doc.add_paragraph(plano_texto)
    if logotipo is not None:
        doc.add_picture(logotipo, width=Inches(1.5))
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ------------------ EXECUÇÃO ------------------
if gerar:
    if not nome_escola or not nome_professor:
        st.warning("⚠️ Preencha Nome da Escola e Nome do Professor.")
    else:
        with st.spinner("Gerando plano profissional..."):
            plano = gerar_plano()
        st.success("✅ Plano gerado com sucesso!")
        st.markdown(plano)
        # Download TXT
        st.download_button("📥 Baixar em TXT", plano, "plano_de_aula.txt")
        # Download Word
        word_file = gerar_word(plano)
        st.download_button("📄 Baixar em Word (.docx)", word_file, "plano_de_aula.docx")
