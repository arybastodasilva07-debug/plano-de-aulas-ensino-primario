import streamlit as st

st.set_page_config(page_title="Plano de Aula Angola Completo", layout="wide")

# --- BASE DE DATA CURRICULAR (INIDI) ---
# Esta estrutura armazena o conhecimento de todos os manuais
DADOS_CURRICULO = {
    "6a Classe": {
        "Geografia": {
            "A Terra e o Universo": {
                "sumario": "O Sistema Solar e a posição da Terra",
                "obj": "Identificar os astros do sistema solar.",
                "fases": ["Revisão: O que é o Universo?", "Explicação: Os 8 planetas e o Sol.", "Atividade: Esquema do sistema solar.", "Controle: Nomear os planetas rochosos."]
            },
            "Movimentos da Terra": {
                "sumario": "Rotação, Translação e as Estações",
                "obj": "Compreender a sucessão dos dias e noites.",
                "fases": ["Pergunta motivadora sobre o dia e a noite.", "Uso do globo para demonstrar a rotação.", "Exercício de desenho das estações.", "Resumo sobre o ano bissexto."]
            },
            "Representação da Terra": {
                "sumario": "Mapas, Globos e Coordenadas",
                "obj": "Interpretar escalas e legendas em mapas.",
                "fases": ["Análise de um mapa de Angola.", "Explicação sobre latitude e longitude.", "Localização de pontos no mapa.", "TPC: Identificar países vizinhos."]
            }
        },
        "Historia": {
            "A Expansao Colonial": {
                "sumario": "Causas e consequências da chegada dos europeus",
                "obj": "Analisar a exploração colonial em África.",
                "fases": ["Contexto das grandes navegações.", "A chegada de Diogo Cão ao Zaire.", "Debate sobre o comércio de escravos.", "Avaliação: Impacto na cultura local."]
            },
            "Resistencia em Angola": {
                "sumario": "Reinos de Angola e a Luta contra a ocupação",
                "obj": "Valorizar figuras históricas como Njinga Mbandi.",
                "fases": ["Biografia da Rainha Njinga.", "As táticas de guerrilha dos reinos.", "Leitura de textos históricos.", "Questionário sobre a resistência."]
            }
        },
        "Matematica": {
            "Numeros Naturais": {
                "sumario": "Leitura e escrita de números até à classe dos milhões",
                "obj": "Dominar a numeração decimal.",
                "fases": ["Revisão da classe dos milhares.", "Exercícios de decomposição numérica.", "Ditado de números grandes.", "Resolução de problemas de soma/subtração."]
            },
            "Geometria": {
                "sumario": "Ângulos, Triângulos e Quadriláteros",
                "obj": "Classificar figuras geométricas planas.",
                "fases": ["Identificação de formas na sala.", "Uso da régua e esquadro.", "Construção de polígonos.", "Cálculo de perímetros simples."]
            }
        }
    },
    "5a Classe": {
        "Ciencias da Natureza": {
            "O Solo": {
                "sumario": "Tipos de solo e sua importância para a agricultura",
                "obj": "Diferenciar solos férteis de solos áridos.",
                "fases": ["Observação de amostras de terra.", "Explicação sobre a erosão.", "Experiência de permeabilidade.", "Conclusão sobre a conservação do solo."]
            }
        }
    },
    "1a Classe": {
        "Estudo do Meio": {
            "A Familia": {
                "sumario": "A composição da família e o parentesco",
                "obj": "Identificar os membros da família próxima.",
                "fases": ["Desenho da árvore genealógica.", "Conversa sobre os deveres de cada um.", "Jogo de nomes (Pai, Mãe, Avós).", "Atividade: Quem mora comigo?"]
            }
        }
    }
}

# --- INTERFACE DO UTILIZADOR ---
st.title("🇦🇴 Plano de Aula Digital - Versão Integral")
st.subheader("Ferramenta de Apoio ao Professor do Ensino Primário")

with st.sidebar:
    st.header("📍 Localização do Conteúdo")
    classe_sel = st.selectbox("Escolha a Classe", list(DADOS_CURRICULO.keys()) + ["2a Classe", "3a Classe", "4a Classe", "Iniciacao"])
    
    # Lógica de Disciplinas Automática
    if "5a" in classe_sel or "6a" in classe_sel:
        lista_disc = ["Lingua Portuguesa", "Matematica", "Ciencias da Natureza", "Historia", "Geografia", "Ed. Moral e Civica"]
    else:
        lista_disc = ["Lingua Portuguesa", "Matematica", "Estudo do Meio", "Ed. Fisica", "Ed. Artistica"]
    
    disc_sel = st.selectbox("Escolha a Disciplina", sorted(lista_disc))

# Seletor de Temas (Botão que você pediu!)
temas_do_manual = DADOS_CURRICULO.get(classe_sel, {}).get(disc_sel, {})
tema_escolhido = st.selectbox("🎯 Selecione o Tema do Manual:", ["-- Consultar Manual --"] + list(temas_do_manual.keys()))

# Variáveis Automáticas
v_sum, v_obj, v_fases = "", "", ["", "", "", ""]

if tema_escolhido != "-- Consultar Manual --":
    dados = temas_do_manual[tema_escolhido]
    v_sum, v_obj, v_fases = dados["sumario"], dados["obj"], dados["fases"]

# --- CAMPOS DE EDIÇÃO ---
st.divider()
tab1, tab2 = st.tabs(["📄 Estrutura do Plano", "⚙️ Metodologia e Materiais"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        sumario = st.text_area("Sumário", value=v_sum)
        obj = st.text_area("Objetivo Específico", value=v_obj)
    with c2:
        st.write("**Desenvolvimento (Fases Didáticas)**")
        f1 = st.text_input("I/M (Introdução)", value=v_fases[0])
        f2 = st.text_input("M/A (Mediação)", value=v_fases[1])
        f3 = st.text_input("D/C (Domínio)", value=v_fases[2])
        f4 = st.text_input("C/A (Controle)", value=v_fases[3])

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        metodo = st.text_input("Método", value="Expositivo/Dialogal")
        meios = st.text_input("Meios Didáticos", value="Quadro, Giz, Manual")
    with col_b:
        avaliacao = st.selectbox("Avaliação", ["Formativa", "Diagnóstica", "Sumativa"])
        tempo = st.text_input("Tempo", "45 min")

# --- GERADOR FINAL ---
if st.button("💾 GERAR PLANO COMPLETO PARA COPIAR"):
    resultado = f"""
ANGOLA - ENSINO PRIMÁRIO
CLASSE: {classe_sel} | DISCIPLINA: {disc_sel} | TEMPO: {tempo}
SUMÁRIO: {sumario}
OBJECTIVO: {obj}
MÉTODO: {metodo} | MEIOS: {meios}
AVALIAÇÃO: {avaliacao}

DESENVOLVIMENTO:
- I/M: {f1}
- M/A: {f2}
- D/C: {f3}
- C/A: {f4}
"""
    st.code(resultado)
    st.success("Tudo pronto! Basta clicar no ícone de copiar no canto da caixa acima.")
