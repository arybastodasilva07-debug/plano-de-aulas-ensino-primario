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

# ---------------- CURRÍCULO ----------------
curriculo = {

    # ================= 1ª CLASSE (OFICIAL) =================
    "1ª Classe": {

        "Língua Portuguesa": {
            "TEMA 1 - QUEM SOU EU?": [
                "Eu sou",
                "Eu chamo-me",
                "Identificar pessoas",
                "Expressões de delicadeza",
                "Grafismos",
                "História: O Sapo e o Ovo"
            ],
            "TEMA 2 – A MINHA FAMÍLIA E EU": [
                "A família da Ana",
                "O alfabeto",
                "Estudo da letra I",
                "Estudo da letra O",
                "Estudo da letra U",
                "Estudo da letra E",
                "Estudo da letra A",
                "Vogais nasais",
                "Ditongos orais",
                "Ditongos nasais"
            ],
            "TEMA 3 – EU VOU À ESCOLA": [
                "Estudo da letra P",
                "Estudo da letra B",
                "Estudo da letra M",
                "Estudo da letra T",
                "Estudo da letra D",
                "Estudo da letra Ç",
                "Estudo da letra S",
                "Estudo da letra Z"
            ],
            "TEMA 4 – O MEU CORPO E EU": [
                "Estudo da letra N",
                "Estudo da letra L",
                "Estudo da letra X",
                "Estudo da letra F",
                "Higiene corporal",
                "Estudo da letra V",
                "Estudo da letra G",
                "Estudo da letra J",
                "Estudo da letra C",
                "Estudo da letra Q",
                "Estudo da letra R"
            ],
            "TEMA 5 – OS ANIMAIS QUE EU CONHEÇO": [
                "Estudo da letra H",
                "Estudo da letra Y",
                "Estudo da letra W",
                "Som NH",
                "Som LH",
                "Som CH",
                "Som AR",
                "Som OL",
                "Som AM",
                "Som UM"
            ]
        },

        "Estudo do Meio": {
            "TEMA 1 - A DESCOBERTA DE SI PRÓPRIO": [
                "A minha identificação",
                "O meu corpo",
                "Órgãos dos sentidos",
                "Saúde do corpo",
                "Higiene do corpo",
                "Higiene alimentar",
                "Posturas correctas, repouso e sono",
                "Vacinas"
            ],
            "TEMA 2 - A FAMÍLIA": [
                "Membros da família",
                "Convivência com outras pessoas"
            ],
            "TEMA 3 - A HABITAÇÃO": [
                "Habitação",
                "Localização da habitação",
                "Compartimentos da habitação",
                "Habitação como lugar de convivência",
                "Cuidados com a casa"
            ],
            "TEMA 4 - A ESCOLA": [
                "A minha escola",
                "Localização da escola",
                "Compartimentos da escola",
                "Sala de aula",
                "Cuidados com a escola",
                "Material escolar",
                "Comunidade escolar"
            ],
            "TEMA 5 - ALIMENTAÇÃO": [
                "Necessidade de alimentação",
                "Alimentação rica e variada",
                "O que devemos comer",
                "Alimentos na nossa dieta",
                "Fonte dos alimentos",
                "Cuidados com os alimentos"
            ],
            "TEMA 6 - O VESTUÁRIO": [
                "Tipos de vestuário",
                "Materiais têxteis",
                "Higiene do vestuário"
            ],
            "TEMA 7 - A SEGURANÇA": [
                "Itinerários",
                "Sinais de trânsito",
                "Regras de trânsito",
                "Cuidados com líquidos inflamáveis e objectos perigosos"
            ],
            "TEMA 8 – AS PLANTAS": [
                "Estrutura das plantas",
                "Importância das plantas",
                "Cuidados com as plantas"
            ],
            "TEMA 9 – OS ANIMAIS": [
                "Animais domésticos e selvagens",
                "Estrutura dos animais",
                "Importância dos animais"
            ]
        },

        "Matemática": {
            "TEMA 1 – GEOMETRIA": [
                "Relações espaciais",
                "Sólidos geométricos",
                "Figuras geométricas planas",
                "Linhas rectas, curvas e quebradas",
                "Linhas abertas e fechadas"
            ],
            "TEMA 2 – NÚMEROS, CONJUNTOS E OPERAÇÕES": [
                "Números naturais até 10",
                "Números naturais até 20",
                "Conjuntos",
                "Números naturais até 50",
                "Números naturais até 100",
                "Adição",
                "Subtracção",
                "Multiplicação por 2, 3 e 4",
                "Divisão por 2, 3 e 4"
            ],
            "TEMA 3 – GRANDEZAS E MEDIDAS": [
                "Comprimento",
                "Massa",
                "Capacidade",
                "Relações temporais",
                "Dias da semana",
                "Dinheiro e moeda angolana"
            ]
        },

        "Educação Manual e Plástica": {
            "TEMA 1 – O DESENHO": [
                "Risco",
                "Traço e tracejo",
                "Pontos",
                "Rasgagem e colagem"
            ],
            "TEMA 2 – A PINTURA": [
                "Impressão e estampagem",
                "Digitintas",
                "Recorte e colagem"
            ],
            "TEMA 3 – A MODELAGEM": [
                "Preparar e amassar barro",
                "Separar e enrolar",
                "Modelagem com barro e plasticina"
            ],
            "TEMA 4 – AS CONSTRUÇÕES": [
                "Dobragem",
                "Recorte e embrulho",
                "Composição e colagem",
                "Construção com materiais diversos"
            ]
        },

        "Educação Musical": {
            "TEMA 1 – A VOZ": [
                "Pequenas canções",
                "Sons naturais e artificiais",
                "Canções populares"
            ],
            "TEMA 2 – O CORPO": [
                "Percussão corporal",
                "Reprodução de batimentos"
            ],
            "TEMA 3 – INICIAÇÃO À TEORIA DA MÚSICA": [
                "Pauta musical",
                "Notas Ré e Mi"
            ],
            "TEMA 4 – OS INSTRUMENTOS MUSICAIS": [
                "Instrumentos de percussão",
                "Audição de sons",
                "Jogos musicais"
            ],
            "TEMA 5 – INICIAÇÃO À TEORIA DA MÚSICA II": [
                "Notas Fá e Sol"
            ]
        },

        "Educação Física": {
            "TEMA 1 – Ginástica básica": [
                "Deslocamento",
                "Salto",
                "Lançamento",
                "Trepar",
                "Equilíbrio"
            ],
            "TEMA 2 – Ginástica rítmica": [
                "Ritmo"
            ],
            "TEMA 3 – Atletismo": [
                "Corrida de velocidade",
                "Corrida de resistência"
            ],
            "TEMA 4 – Jogos": [
                "Jogos com bola",
                "Jogos de correr",
                "Jogos de saltar",
                "Jogos sensoriais"
            ]
        }
    }
}
