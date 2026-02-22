import streamlit as st
from openai import OpenAI
from docx import Document
from docx.shared import Inches
import io
import os

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="Plano de Aula - INIDE Angola", layout="wide")
st.title("🇦🇴 SISTEMA PROFISSIONAL DE PLANO DE AULA")
st.subheader("Ensino Primário (Iniciação à 6ª Classe)")

# ---------------- OPENAI CLIENT ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ API Key não configurada. Vá em Settings → Secrets e adicione OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- CURRÍCULO ESTRUTURADO (EXEMPLO) ----------------
# Estrutura: Classe -> Disciplina -> Tema -> Subtema -> [Lista de Sumários]
curriculo = {
    "1ª Classe": {
        "Língua Portuguesa": {
            "TEMA 2 – A MINHA FAMÍLIA E EU": {
                "Estudo das Vogais": ["Letra I", "Letra O", "Letra U", "Letra E", "Letra A"],
                "Sons e Ditongos": ["Vogais nasais", "Ditongos orais", "Ditongos nasais"]
            },
            "TEMA 3 – EU VOU À ESCOLA": {
                "Consoantes Iniciais": ["Estudo da letra P", "Estudo da letra B", "Estudo da letra M"],
                "Consoantes Dentais": ["Estudo da letra T", "Estudo da letra D"]
            }
        },
        "Estudo do Meio": {
            "TEMA 1 - A DESCOBERTA DE SI PRÓPRIO": {
                "O Meu Corpo": ["Identificação pessoal", "Partes do corpo", "Órgãos dos sentidos"],
                "Higiene e Saúde": ["Higiene corporal", "Higiene alimentar", "Vacinas"]
            },
            "TEMA 5 - ALIMENTAÇÃO": {
                "Importância": ["Necessidade de alimentação", "Alimentação rica e variada"],
                "Origem e Cuidados": ["Fonte dos alimentos", "Cuidados a ter com os alimentos"]
            }
        },
        "Matemática": {
            "TEMA 2 – NÚMEROS E OPERAÇÕES": {
                "Números Naturais": ["Números de 1 a 10", "Números de 11 a 20", "A Dezena"],
                "Operações": ["Adição até 9", "Subtracção até 9", "Algoritmo vertical"]
            }
        }
    },
    "2ª Classe": {
        "Língua Portuguesa": {
            "A Minha Escola": {
                "Textos de Apoio": ["O encontro", "Pelo caminho", "A queda da Vera"],
                "Gramática": ["A frase", "Pontuação básica"]
            }
        }
    }
}

# ---------------- SIDEBAR (LÓGICA DE CASCATA) ----------------
with st.sidebar:
    st.header("🏫 Identificação")
    nome_escola = st.text_input("Nome da Escola")
    nome_professor = st.text_input("Nome do Professor")
    trimestre = st.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
    logotipo = st.file_uploader("Logotipo da Escola (opcional)", type=["png","jpg","jpeg"])

    st.header("📚 Dados da Aula")
    
    # Seleção de Classe
    classe_sel = st.selectbox("Classe", list(curriculo.keys()))
    
    # Seleção de Disciplina
    disciplinas = list(curriculo[classe_sel].keys())
    disciplina_sel = st.selectbox("Disciplina", disciplinas)
    
    # Seleção de Tema
    temas = list(curriculo[classe_sel][disciplina_sel].keys())
    tema_sel = st.selectbox("Tema", temas)
    
    # Seleção de Subtema
    subtemas_dict = curriculo[classe_sel][disciplina_sel][tema_sel]
    subtema_sel = st.selectbox("Subtema", list(subtemas_dict.keys()))
    
    # Seleção de Sumário (O que o usuário pediu: aumenta depois do subtema)
    lista_sumarios = subtemas_dict[subtema_sel]
    sumario_sel = st.selectbox("Sumário (Assunto da Aula)", lista_sumarios)
    
    aula_numero = st.number_input("Aula nº", min_value=1, step=1)
    tempo = "45 minutos"

    gerar = st.button("🧠 Gerar Plano de Aula")

# ---------------- FUNÇÃO PARA GERAR PLANO COM IA ----------------
def gerar_plano():
    prompt = f"""
    Gere um plano de aula completo baseado no currículo oficial do INIDE (Angola).
    
    DADOS:
    Escola: {nome_escola} | Professor: {nome_professor}
    Disciplina: {disciplina_sel} | Classe: {classe_sel}
    Trimestre: {trimestre} | Tempo: {tempo} | Aula nº: {aula_numero}
    Unidade Temática (Tema): {tema_sel}
    Subtema: {subtema_sel}
    Sumário Específico: {sumario_sel}

    ESTRUTURA OBRIGATÓRIA:
    1. Objectivos Operacionais (O que o aluno deve saber fazer)
    2. Conteúdo Detalhado
    3. Meios de Ensino (Material Didáctico)
    4. Métodos de Ensino
    5. Fases da Aula (Procedimentos Didácticos):
       - Introdução e Motivação
       - Mediação e Assimilação
       - Domínio e Consolidação
       - Controle e Avaliação
    6. Tarefa para Casa
    
    Use linguagem pedagógica formal de Angola.
    """
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Especialista em educação primária angolana e normas do INIDE."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return resposta.choices[0].message.content
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return None

# ---------------- FUNÇÃO WORD ----------------
def gerar_word(plano_texto):
    doc = Document()
    doc.add_heading("REPÚBLICA DE ANGOLA", level=1)
    header = doc.add_paragraph()
    header.add_run(f"Escola: {nome_escola}\nProfessor: {nome_professor}\n").bold = True
    header.add_run(f"Disciplina: {disciplina_sel} | Classe: {classe_sel}\nSumário: {sumario_sel}")
    
    doc.add_heading("PLANO DE AULA", level=2)
    doc.add_paragraph(plano_texto)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ---------------- EXECUÇÃO NO CORPO DO APP ----------------
if gerar:
    if not nome_escola or not nome_professor:
        st.warning("⚠️ Preencha os dados de identificação na barra lateral.")
    else:
        with st.spinner("A IA está redigindo o seu plano..."):
            plano_gerado = gerar_plano()
            
            if plano_gerado:
                st.success("✅ Plano Gerado!")
                st.markdown(plano_gerado)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 Baixar em Word", gerar_word(plano_gerado), "plano.docx")
                with col2:
                    st.download_button("📄 Baixar em TXT", plano_gerado, "plano.txt")

# Rodapé informativo
st.info("Nota: Este sistema utiliza o modelo GPT-4o-mini para alinhar os temas do INIDE com metodologias activas.")











