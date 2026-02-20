import streamlit as st
import openai
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Plano de Aula - INIDE Angola", layout="wide")

st.title("🇦🇴 GERADOR DE PLANO DE AULA")
st.subheader("Ensino Primário (Iniciação à 6ª Classe) - Baseado no INIDE")

# API KEY (colocar no secrets do Streamlit Cloud ou .env)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ------------------ SIDEBAR ------------------
with st.sidebar:
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

    tempo = st.selectbox("Tempo", ["45 minutos"])

    aula_numero = st.number_input("Aula nº", min_value=1, step=1)

    unidade = st.text_input("Unidade Temática")

    subtema = st.text_input("Subtema ou Sumário")

    gerar = st.button("🧠 Gerar Plano de Aula")


# ------------------ FUNÇÃO IA ------------------

def gerar_plano_ia():
    prompt = f"""
    Você é um especialista em educação primária em Angola.

    Gere um plano de aula COMPLETO com base no programa oficial do INIDE e nos manuais actualizados do ensino primário.

    Dados:
    Disciplina: {disciplina}
    Classe: {classe}
    Tempo: {tempo}
    Aula nº: {aula_numero}
    Unidade temática: {unidade}
    Subtema: {subtema}

    Se o subtema for muito amplo, divida em 2 ou mais aulas de 45 minutos.

    Estrutura obrigatória:

    1. Objetivo Geral (ligado à unidade temática)
    2. Objetivos da Aula
    3. Conteúdo
    4. Material Didáctico
    5. Metodologia
    6. Actividades Chave
    7. Tipo de Avaliação
    8. Procedimentos da Aula divididos em:
        - Introdução
        - Desenvolvimento
        - Consolidação
        - Avaliação
        - Tarefa para Casa

    Use linguagem formal pedagógica.
    Contextualize à realidade angolana.
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Especialista em planos de aula do ensino primário angolano."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    return resposta["choices"][0]["message"]["content"]


# ------------------ GERAÇÃO ------------------

if gerar:
    if unidade == "" or subtema == "":
        st.warning("⚠️ Preencha a Unidade Temática e o Subtema.")
    else:
        with st.spinner("Gerando plano de aula..."):
            plano = gerar_plano_ia()

        st.success("✅ Plano gerado com sucesso!")
        st.markdown(plano)

        # BOTÃO PARA DOWNLOAD
        st.download_button(
            label="📥 Baixar Plano em .txt",
            data=plano,
            file_name="plano_de_aula.txt",
            mime="text/plain"
        )
