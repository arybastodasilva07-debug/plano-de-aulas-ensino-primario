import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Gerador INIDE Angola", layout="wide", page_icon="🇦🇴")

# --- BASE DE DADOS DE DISCIPLINAS POR CLASSE (PADRÃO INIDE) ---
DISCIPLINAS_POR_CLASSE = {
    "Iniciação": ["Língua Portuguesa", "Matemática", "Estudo do Meio", "Educação Artística", "Educação Física"],
    "1ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio", "Educação Artística", "Educação Física"],
    "2ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio", "Educação Artística", "Educação Física"],
    "3ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio", "Educação Artística", "Educação Física", "Educação Moral e Cívica"],
    "4ª Classe": ["Língua Portuguesa", "Matemática", "Estudo do Meio", "Educação Artística", "Educação Física", "Educação Moral e Cívica"],
    "5ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia", "Educação Moral e Cívica", "Educação Visual e Plástica", "Educação Musical", "Educação Física"],
    "6ª Classe": ["Língua Portuguesa", "Matemática", "Ciências da Natureza", "História", "Geografia", "Educação Moral e Cívica", "Educação Visual e Plástica", "Educação Musical", "Educação Física"]
}

# --- EXEMPLOS DE TEMAS/CONTEÚDOS AUTOMÁTICOS (EXEMPLO PARA TESTE) ---
# Aqui pode-se expandir com todos os manuais
BASE_CONTEUDO = {
    "Geografia": {
        "A Terra e o Universo": {
            "obj_geral": "Compreender a organização do sistema solar.",
            "obj_aula": "Identificar os planetas e a posição da Terra no sistema solar.",
            "conteudo": "O Sol, os oito planetas, satélites e astros menores.",
            "metodologia": "Método Expositivo e Elaboração Conjunta.",
            "actividades": "Observação de gravuras e desenho do sistema solar no caderno.",
            "material": "Manual do aluno, Globo terrestre, Cartazes.",
            "fases": ["Revisão de conceitos de céu e estrelas", "Explicação sobre a centralidade do sol", "Exercício de identificação dos planetas", "Pergunta de controlo sobre o maior planeta"]
        }
    },
    "História": {
        "A Resistência em Angola": {
            "obj_geral": "Valorizar a luta dos povos de Angola contra a ocupação.",
            "obj_aula": "Descrever o papel da Rainha Njinga Mbandi na resistência.",
            "conteudo": "A resistência dos reinos do Ndongo e Matamba.",
            "metodologia": "Método Narrativo e Trabalho Independente.",
            "actividades": "Leitura de texto biográfico e debate sobre tácticas de guerra.",
            "material": "Manual, mapas históricos, ilustrações.",
            "fases": ["Introdução sobre a chegada dos portugueses", "Narração da vida de Njinga Mbandi", "Debate sobre a coragem da rainha", "Resumo das ideias chaves"]
        }
    }
}

# --- INTERFACE ---
st.title("🇦🇴 Sistema Automático de Planos de Aula")
st.markdown("### Alinhado ao Programa Curricular do INIDE")

# Janela 1: Identificação
with st.expander("📂 1. IDENTIFICAÇÃO E DADOS GERAIS", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        classe = st.selectbox("Classe", list(DISCIPLINAS_POR_CLASSE.keys()))
        tempo = st.selectbox("Tempo de Aula", ["45 min", "90 min"])
    with c2:
        disciplina = st.selectbox("Disciplina", DISCIPLINAS_POR_CLASSE[classe])
        aula_no = st.number_input("Aula Nº", min_value=1, step=1)
    with c3:
        tema = st.text_input("Tema Geral", placeholder="Ex: A Terra e o Universo")
        sumario = st.text_input("Sumário ou Subtema", placeholder="Ex: O Sistema Solar")

# Lógica de Sugestão Automática
sugestao = BASE_CONTEUDO.get(disciplina, {}).get(tema, {})

# Janela 2: Objectivos e Conteúdo
with st.expander("🎯 2. OBJECTIVOS E CONTEÚDOS"):
    c_obj1, c_obj2 = st.columns(2)
    with c_obj1:
        obj_geral = st.text_area("Objectivos Gerais", value=sugestao.get("obj_geral", ""))
        obj_aula = st.text_area("Objectivos da Aula", value=sugestao.get("obj_aula", ""))
    with c_obj2:
        conteudo = st.text_area("Conteúdo Teórico", value=sugestao.get("conteudo", ""))
        material = st.text_input("Material Didáctico", value=sugestao.get("material", "Quadro, giz, manual, apagador"))

# Janela 3: Metodologia e Estratégia
with st.expander("⚙️ 3. METODOLOGIA E ACTIVIDADES"):
    c_met1, c_met2 = st.columns(2)
    with c_met1:
        metodologia = st.text_input("Metodologias de Ensino", value=sugestao.get("metodologia", "Método Expositivo"))
        avaliacao = st.selectbox("Tipo de Avaliação", ["Formativa (Contínua)", "Diagnóstica", "Sumativa"])
    with c_met2:
        actividades = st.text_area("Actividades Chaves", value=sugestao.get("actividades", ""))

# Janela 4: Fases da Aula (Desenvolvimento)
with st.expander("⏳ 4. FASES DA AULA (DESENVOLVIMENTO)"):
    f_fases = sugestao.get("fases", ["", "", "", ""])
    f1, f2 = st.columns(2)
    with f1:
        intro = st.text_area("I/M (Introdução e Motivação)", value=f_fases[0])
        media = st.text_area("M/A (Mediação e Assimilação)", value=f_fases[1])
    with f2:
        dominio = st.text_area("D/C (Domínio e Consolidação)", value=f_fases[2])
        controle = st.text_area("C/A (Controle e Avaliação)", value=f_fases[3])

# Botão de Sugestão de IA Realista (Contexto Angola)
if st.button("🤖 Sugerir Atividades (Realidade Local)"):
    st.info(f"Sugestão para {tema}: 'Use exemplos do mercado local e materiais do meio (pedras, sementes) para ilustrar os conceitos, adaptando à realidade da província.'")

# Botão Final
if st.button("📝 GERAR PLANO COMPLETO"):
    st.success("Plano de aula gerado com sucesso!")
    resultado = f"""
    --- PLANO DE AULA FORMATADO ---
    CLASSE: {classe} | DISCIPLINA: {disciplina} | TEMPO: {tempo} | AULA Nº: {aula_no}
    TEMA: {tema} | SUMÁRIO: {sumario}
    
    OBJECTIVOS GERAIS: {obj_geral}
    OBJECTIVOS DA AULA: {obj_aula}
    CONTEÚDO: {conteudo}
    MATERIAL: {material}
    METODOLOGIA: {metodologia}
    ACTIVIDADES CHAVE: {actividades}
    AVALIAÇÃO: {avaliacao}
    
    DESENVOLVIMENTO:
    1. I/M: {intro}
    2. M/A: {media}
    3. D/C: {dominio}
    4. C/A: {controle}
    -------------------------------
    """
    st.code(resultado, language="text")
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

