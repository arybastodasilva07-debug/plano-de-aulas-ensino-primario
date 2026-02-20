import streamlit as st

st.set_page_config(page_title="Plano Automatico Angola", layout="wide")

# --- BASE DE DADOS INTEGRADA (Exemplo de 6ª e 1ª Classe) ---
# Aqui o programa guarda o conhecimento pedagógico
DADOS_CURRICULO = {
    "6a Classe": {
        "Geografia": {
            "A Terra e o Universo": {
                "sumario": "O Sistema Solar: Planetas e Astros",
                "objetivo": "Identificar os componentes do sistema solar e a posição da Terra.",
                "conteudo": "Sol, planetas rochosos e gasosos, satélites naturais e cometas.",
                "metodo": "Expositivo e Observação de Gravuras",
                "intro": "Revisão sobre o conceito de astro e céu noturno.",
                "mediacao": "Explicação sobre a centralidade do Sol e os 8 planetas.",
                "dominio": "Desenho do sistema solar no caderno.",
                "controle": "Pergunta: Qual o maior planeta do sistema solar?"
            },
            "Movimentos da Terra": {
                "sumario": "Rotação e Translação e suas consequências",
                "objetivo": "Explicar a sucessão dos dias/noites e das estações do ano.",
                "conteudo": "Eixo de inclinação, órbita elíptica, 24h e 365 dias.",
                "metodo": "Demonstração Prática (Globo e Lanterna)",
                "intro": "Pergunta aos alunos: Porque é que o Sol 'nasce' e 'se põe'?",
                "mediacao": "Demonstração do movimento de rotação usando um globo.",
                "dominio": "Esquematização dos movimentos no caderno.",
                "controle": "Avaliação sobre a diferença entre dia e noite."
            }
        }
    },
    "1a Classe": {
        "Estudo do Meio": {
            "O Corpo Humano": {
                "sumario": "As partes principais do corpo: Cabeça, tronco e membros",
                "objetivo": "Reconhecer e nomear as partes do próprio corpo.",
                "conteudo": "Estrutura externa do corpo humano.",
                "metodo": "Jogo Didáctico e Canções",
                "intro": "Canção 'Cabeça, Ombro, Joelho e Pé'.",
                "mediacao": "Identificação das partes no colega.",
                "dominio": "Pintura de um boneco com as partes indicadas.",
                "controle": "Jogo de apontar: 'Onde está o teu cotovelo?'"
            }
        }
    }
}

st.title("🚀 Gerador de Planos Automático")
st.info("Selecione a Classe e a Disciplina para ver a mágica acontecer!")

# --- SELEÇÃO DINÂMICA ---
with st.sidebar:
    classe_sel = st.selectbox("Classe", ["6a Classe", "1a Classe", "2a Classe", "3a Classe", "4a Classe", "5a Classe"])
    
    # Filtra disciplinas que temos na base de dados
    if classe_sel in DADOS_CURRICULO:
        discs_disponiveis = list(DADOS_CURRICULO[classe_sel].keys())
    else:
        discs_disponiveis = ["Selecione outra classe"]
        
    disc_sel = st.selectbox("Disciplina", discs_disponiveis)

# --- LÓGICA DE PREENCHIMENTO AUTOMÁTICO ---
temas_disponiveis = {}
if classe_sel in DADOS_CURRICULO and disc_sel in DADOS_CURRICULO[classe_sel]:
    temas_disponiveis = DADOS_CURRICULO[classe_sel][disc_sel]

tema_sel = st.selectbox("Escolha o Tema do Programa:", ["-- Selecionar Tema --"] + list(temas_disponiveis.keys()))

# Inicializar variáveis vazias
val_sumario, val_obj, val_cont, val_met, val_int, val_med, val_dom, val_con = [""] * 8

# Se um tema for escolhido, carregar os dados
if tema_sel != "-- Selecionar Tema --":
    dados = temas_disponiveis[tema_sel]
    val_sumario = dados["sumario"]
    val_obj = dados["objetivo"]
    val_cont = dados["conteudo"]
    val_met = dados["metodo"]
    val_int = dados["intro"]
    val_med = dados["mediacao"]
    val_dom = dados["dominio"]
    val_con = dados["controle"]

# --- INTERFACE DE EDIÇÃO (Campos preenchidos) ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    tema_final = st.text_input("Tema", value=tema_sel if tema_sel != "-- Selecionar Tema --" else "")
    sumario_final = st.text_area("Sumário", value=val_sumario)
    objetivo_final = st.text_area("Objetivo", value=val_obj)

with col2:
    conteudo_final = st.text_area("Conteúdo Teórico", value=val_cont)
    metodo_final = st.text_input("Método", value=val_met)
    material_final = st.text_input("Material", value="Manual, Quadro, Giz")

st.subheader("⏳ Fases Didácticas (Preenchidas Automaticamente)")
f1, f2 = st.columns(2)
with f1:
    intro_final = st.text_area("I/M", value=val_int)
    med_final = st.text_area("M/A", value=val_med)
with f2:
    dom_final = st.text_area("D/C", value=val_dom)
    cont_final = st.text_area("C/A", value=val_con)

if st.button("📄 FINALIZAR PLANO"):
    st.success("Plano Gerado com Sucesso!")
    # Aqui viria o texto final formatado...
