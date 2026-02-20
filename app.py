import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Gestor Escolar Angola", layout="wide")

# Título e Cabeçalho Oficial
st.title("🇦🇴 SISTEMA DE PLANEAMENTO PEDAGÓGICO")
st.caption("Ensino Primário (Iniciação à 6ª Classe) - Republica de Angola")

# --- BARRA LATERAL (BIBLIOTECA E DOSIFICAÇÃO) ---
with st.sidebar:
    st.header("📚 Centro de Recursos")
    st.info("Consulte os manuais e a dosificação anual abaixo.")
    
    classe = st.selectbox("Selecione a Classe", 
                         ["Iniciacao", "1 Classe", "2 Classe", "3 Classe", "4 Classe", "5 Classe", "6 Classe"])
    
    # Lógica de Disciplinas Dinâmicas
    disc_base = ["Lingua Portuguesa", "Matematica", "Educacao Moral e Civica", "Educacao Fisica", "Educacao Visual e Plastica"]
    if classe in ["5 Classe", "6 Classe"]:
        disciplinas = sorted(disc_base + ["Historia", "Geografia", "Ciencias da Natureza"])
    else:
        disciplinas = sorted(disc_base + ["Estudo do Meio"])
    
    disciplina = st.selectbox("Disciplina", disciplinas)
    
    st.divider()
    st.header("📅 Dosificacao Mensal")
    mes = st.selectbox("Mes de Trabalho", ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro"])
    semana = st.radio("Semana", ["1a Semana", "2a Semana", "3a Semana", "4a Semana"])

# --- ÁREA PRINCIPAL: DOSIFICAÇÃO AUTOMÁTICA ---
st.subheader(f"📌 Sugestao de Conteudo: {disciplina}")
# Exemplo de base de dados simplificada para Geografia 6a Classe
if disciplina == "Geografia" and classe == "6 Classe":
    st.warning("Conteudo da Dosificacao: A Terra e o Universo: O Sistema Solar (Manual pág. 12)")
else:
    st.warning("Consulte o Manual Fisico para este conteudo ou adicione a dosificacao no codigo.")

st.divider()

# --- FORMULÁRIO DO PLANO DE AULA ---
st.subheader("📝 Elaboracao do Plano de Aula")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    tema = st.text_input("Tema da Unidade")
    sumario = st.text_area("Sumario")
with c2:
    obj_geral = st.text_area("Objetivo Geral")
    obj_especifico = st.text_area("Objetivos Especificos (Aula)")
with c3:
    tempo = st.text_input("Tempo", "45 min")
    materiais = st.text_area("Materiais Didacticos")

st.divider()
st.subheader("⚙️ Metodologia e Avaliacao")
m1, m2, m3 = st.columns(3)
with m1:
    metodo = st.multiselect("Metodos", ["Expositivo", "Elaboracao Conjunta", "Trabalho Independente", "Observacao"])
with m2:
    actividades = st.text_area("Actividades Chaves")
with m3:
    avaliacao = st.selectbox("Tipo de Avaliacao", ["Formativa (Continua)", "Diagnostica", "Sumativa"])

st.divider()
st.subheader("⏳ Fases Didacticas (Desenvolvimento)")
f1, f2 = st.columns(2)
with f1:
    intro = st.text_area("1. Introducao e Motivacao (Revisao)")
    mediacao = st.text_area("2. Mediacao e Assimilacao (Novo Conteudo)")
with f2:
    dominio = st.text_area("3. Dominio e Consolidacao (Exercicios)")
    controle = st.text_area("4. Controle e Avaliacao (TPC/Resumo)")

# --- BOTÃO DE FINALIZAÇÃO ---
if st.button("💾 VISUALIZAR PLANO FINAL"):
    st.success("Plano pronto para copiar para o Caderno de Planos!")
    st.markdown(f"""
    **{disciplina} - {classe}** | **Tempo:** {tempo}
    
    **Sumario:** {sumario}
    
    **Objectivos:** {obj_especifico}
    
    **Metodo:** {", ".join(metodo)} | **Avaliacao:** {avaliacao}
    
    **Desenvolvimento:**
    * **I/M:** {intro}
    * **M/A:** {mediacao}
    * **D/C:** {dominio}
    * **C/A:** {controle}
    """)
